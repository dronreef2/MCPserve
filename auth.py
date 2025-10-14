"""
Authentication system for MCP Server
Provides API key validation and user management
"""

import os
import hashlib
import secrets
import time
from typing import Dict, Optional, List, Any
import json
import logging

logger = logging.getLogger(__name__)

class AuthManager:
    """Manages API key authentication and user access"""

    def __init__(self, keys_file: str = "api_keys.json"):
        self.keys_file = keys_file
        self.api_keys: Dict[str, Dict[str, Any]] = {}
        self.load_keys()

    def load_keys(self):
        """Load API keys from file"""
        try:
            if os.path.exists(self.keys_file):
                with open(self.keys_file, 'r') as f:
                    self.api_keys = json.load(f)
                logger.info(f"Loaded {len(self.api_keys)} API keys")
            else:
                # Create default admin key
                admin_key = self.generate_key()
                self.api_keys[admin_key] = {
                    'user': 'admin',
                    'role': 'admin',
                    'created': time.time(),
                    'last_used': None,
                    'permissions': ['read', 'write', 'admin']
                }
                self.save_keys()
                logger.info(f"Created default admin key: {admin_key[:8]}...")
        except Exception as e:
            logger.error(f"Error loading API keys: {e}")

    def save_keys(self):
        """Save API keys to file"""
        try:
            with open(self.keys_file, 'w') as f:
                json.dump(self.api_keys, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving API keys: {e}")

    def generate_key(self, length: int = 32) -> str:
        """Generate a secure API key"""
        return secrets.token_urlsafe(length)

    def hash_key(self, key: str) -> str:
        """Hash API key for storage (if needed)"""
        return hashlib.sha256(key.encode()).hexdigest()

    def validate_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate API key and return user info"""
        if api_key in self.api_keys:
            user_info = self.api_keys[api_key].copy()
            # Update last used timestamp
            user_info['last_used'] = time.time()
            self.api_keys[api_key]['last_used'] = time.time()
            self.save_keys()
            return user_info
        return None

    def create_user(self, username: str, role: str = 'user', permissions: List[str] = None) -> str:
        """Create a new user with API key"""
        if permissions is None:
            permissions = ['read']

        api_key = self.generate_key()
        self.api_keys[api_key] = {
            'user': username,
            'role': role,
            'created': time.time(),
            'last_used': None,
            'permissions': permissions
        }
        self.save_keys()
        logger.info(f"Created user {username} with role {role}")
        return api_key

    def revoke_key(self, api_key: str) -> bool:
        """Revoke an API key"""
        if api_key in self.api_keys:
            del self.api_keys[api_key]
            self.save_keys()
            logger.info(f"Revoked API key for user {self.api_keys.get(api_key, {}).get('user', 'unknown')}")
            return True
        return False

    def list_users(self) -> List[Dict[str, Any]]:
        """List all users (admin only)"""
        users = []
        for key, info in self.api_keys.items():
            user_info = info.copy()
            user_info['api_key'] = key[:8] + '...'  # Mask most of the key
            users.append(user_info)
        return users

    def has_permission(self, user_info: Dict[str, Any], permission: str) -> bool:
        """Check if user has specific permission"""
        if not user_info:
            return False

        permissions = user_info.get('permissions', [])
        role = user_info.get('role', 'user')

        # Admin has all permissions
        if role == 'admin':
            return True

        return permission in permissions

# Global auth manager instance
auth_manager = AuthManager()

def require_auth(permission: str = 'read'):
    """Decorator to require authentication and permissions"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Extract API key from request (this would need to be adapted based on your MCP setup)
            api_key = kwargs.get('api_key') or os.getenv('API_KEY')

            if not api_key:
                raise ValueError("API key required")

            user_info = auth_manager.validate_key(api_key)
            if not user_info:
                raise ValueError("Invalid API key")

            if not auth_manager.has_permission(user_info, permission):
                raise ValueError(f"Permission denied: {permission}")

            # Add user info to kwargs
            kwargs['user_info'] = user_info
            return await func(*args, **kwargs)
        return wrapper
    return decorator