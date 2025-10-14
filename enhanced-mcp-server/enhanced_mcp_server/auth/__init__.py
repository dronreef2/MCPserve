"""Sistema de autenticação com API keys."""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import json
from pathlib import Path
from enhanced_mcp_server.config import settings
from enhanced_mcp_server.utils.logging import get_logger

logger = get_logger(__name__)


class APIKey:
    """Representa uma chave API."""

    def __init__(self, key_hash: str, email: str, role: str = "user",
                 created_at: datetime = None, expires_at: datetime = None):
        self.key_hash = key_hash
        self.email = email
        self.role = role
        self.created_at = created_at or datetime.now()
        self.expires_at = expires_at

    def is_expired(self) -> bool:
        """Verifica se a chave expirou."""
        return self.expires_at and datetime.now() > self.expires_at

    def is_valid(self) -> bool:
        """Verifica se a chave é válida."""
        return not self.is_expired()

    def to_dict(self) -> Dict:
        """Converte para dicionário."""
        return {
            "key_hash": self.key_hash,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'APIKey':
        """Cria instância a partir de dicionário."""
        return cls(
            key_hash=data["key_hash"],
            email=data["email"],
            role=data["role"],
            created_at=datetime.fromisoformat(data["created_at"]),
            expires_at=datetime.fromisoformat(data["expires_at"]) if data.get("expires_at") else None,
        )


class AuthManager:
    """Gerenciador de autenticação."""

    def __init__(self, keys_file: str = "api_keys.json"):
        self.keys_file = Path(keys_file)
        self._keys: Dict[str, APIKey] = {}
        self._load_keys()

    def _load_keys(self) -> None:
        """Carrega chaves do arquivo."""
        if self.keys_file.exists():
            try:
                with open(self.keys_file, 'r') as f:
                    data = json.load(f)
                    for key_hash, key_data in data.items():
                        self._keys[key_hash] = APIKey.from_dict(key_data)
                logger.info(f"Loaded {len(self._keys)} API keys")
            except Exception as e:
                logger.error(f"Failed to load API keys: {e}")

    def _save_keys(self) -> None:
        """Salva chaves no arquivo."""
        try:
            data = {key_hash: key.to_dict() for key_hash, key in self._keys.items()}
            with open(self.keys_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save API keys: {e}")

    def _hash_key(self, key: str) -> str:
        """Gera hash da chave API."""
        return hashlib.sha256(key.encode()).hexdigest()

    def generate_api_key(self, email: str, role: str = "user",
                        expires_days: int = None) -> str:
        """Gera uma nova chave API."""
        key = secrets.token_urlsafe(32)
        key_hash = self._hash_key(key)

        expires_at = None
        if expires_days:
            expires_at = datetime.now() + timedelta(days=expires_days)

        api_key = APIKey(key_hash, email, role, expires_at=expires_at)
        self._keys[key_hash] = api_key
        self._save_keys()

        logger.info(f"Generated API key for {email} with role {role}")
        return key

    def validate_api_key(self, key: str) -> Optional[APIKey]:
        """Valida uma chave API."""
        key_hash = self._hash_key(key)
        api_key = self._keys.get(key_hash)

        if api_key and api_key.is_valid():
            return api_key

        return None

    def revoke_api_key(self, key: str) -> bool:
        """Revoga uma chave API."""
        key_hash = self._hash_key(key)
        if key_hash in self._keys:
            del self._keys[key_hash]
            self._save_keys()
            logger.info(f"Revoked API key for hash {key_hash[:8]}...")
            return True
        return False

    def list_api_keys(self) -> List[Dict]:
        """Lista todas as chaves API."""
        return [
            {
                "email": key.email,
                "role": key.role,
                "created_at": key.created_at.isoformat(),
                "expires_at": key.expires_at.isoformat() if key.expires_at else None,
                "is_expired": key.is_expired(),
            }
            for key in self._keys.values()
        ]

    def cleanup_expired_keys(self) -> int:
        """Remove chaves expiradas."""
        expired_keys = [k for k, v in self._keys.items() if v.is_expired()]
        for key in expired_keys:
            del self._keys[key]

        if expired_keys:
            self._save_keys()
            logger.info(f"Cleaned up {len(expired_keys)} expired API keys")

        return len(expired_keys)


# Instância global do gerenciador de autenticação
auth_manager = AuthManager()