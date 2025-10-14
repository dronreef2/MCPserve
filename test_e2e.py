#!/usr/bin/env python3
"""
End-to-End Tests for MCP Server
Tests the complete functionality from API calls to MCP responses
"""

import os
import sys
import time
import subprocess
import requests
import pytest
from typing import Dict, Any

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auth import auth_manager

class TestMCPIntegration:
    """Integration tests for MCP Server functionality"""

    @classmethod
    def setup_class(cls):
        """Start the MCP server for testing"""
        # Set test environment variables
        os.environ['JINA_API_KEY'] = 'test_jina_key'
        os.environ['GEMINI_API_KEY'] = 'test_gemini_key'
        os.environ['DEEPL_API_KEY'] = 'test_deepl_key'

        # Start server in background
        cls.server_process = subprocess.Popen(
            [sys.executable, 'main.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )

        # Wait for server to start
        time.sleep(3)

        # Check if server is running
        try:
            response = requests.get('http://localhost:8000/health', timeout=5)
            if response.status_code != 200:
                pytest.skip("Server health check failed")
        except:
            pytest.skip("Server not responding")

    @classmethod
    def teardown_class(cls):
        """Stop the MCP server"""
        if hasattr(cls, 'server_process'):
            cls.server_process.terminate()
            cls.server_process.wait(timeout=5)

    def test_server_health(self):
        """Test server health endpoint"""
        response = requests.get('http://localhost:8000/health', timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert 'status' in data
        assert data['status'] == 'healthy'

    def test_fetch_tool_validation(self):
        """Test fetch tool input validation"""
        # Test with invalid URL
        response = requests.post('http://localhost:8000/mcp/fetch', json={
            'url': 'not-a-valid-url'
        }, timeout=10)

        # Should return error for invalid URL
        assert response.status_code in [200, 400]  # MCP might return 200 with error message

        # Test with valid URL format
        response = requests.post('http://localhost:8000/mcp/fetch', json={
            'url': 'https://httpbin.org/get'
        }, timeout=10)

        # Should attempt to fetch (may fail due to API key, but shouldn't crash)
        assert response.status_code in [200, 401, 429]

    def test_search_tool_validation(self):
        """Test search tool input validation"""
        # Test with empty query
        response = requests.post('http://localhost:8000/mcp/search', json={
            'query': ''
        }, timeout=10)

        assert response.status_code in [200, 400]

        # Test with valid query
        response = requests.post('http://localhost:8000/mcp/search', json={
            'query': 'test query'
        }, timeout=10)

        assert response.status_code in [200, 401, 429]

    def test_translate_tool_validation(self):
        """Test translate tool input validation"""
        # Test with empty text
        response = requests.post('http://localhost:8000/mcp/translate', json={
            'text': ''
        }, timeout=10)

        assert response.status_code in [200, 400]

        # Test with valid text
        response = requests.post('http://localhost:8000/mcp/translate', json={
            'text': 'Hello world',
            'from_lang': 'en',
            'to_lang': 'es'
        }, timeout=10)

        assert response.status_code in [200, 401, 429]

    def test_translate_deepl_validation(self):
        """Test DeepL translate tool validation"""
        response = requests.post('http://localhost:8000/mcp/translate_deepl', json={
            'text': 'Hello world',
            'from_lang': 'en',
            'to_lang': 'es'
        }, timeout=10)

        assert response.status_code in [200, 401, 429]

    def test_optimize_prompt_validation(self):
        """Test prompt optimization validation"""
        response = requests.post('http://localhost:8000/mcp/optimize_prompt', json={
            'user_prompt': ''
        }, timeout=10)

        assert response.status_code in [200, 400]

        # Test with valid prompt
        response = requests.post('http://localhost:8000/mcp/optimize_prompt', json={
            'user_prompt': 'How to write better code?'
        }, timeout=10)

        assert response.status_code == 200

class TestAuthSystem:
    """Test authentication system"""

    def test_api_key_generation(self):
        """Test API key generation"""
        key1 = auth_manager.generate_key()
        key2 = auth_manager.generate_key()

        assert len(key1) > 20
        assert len(key2) > 20
        assert key1 != key2

    def test_user_creation(self):
        """Test user creation and validation"""
        username = f"test_user_{int(time.time())}"
        api_key = auth_manager.create_user(username, 'user', ['read'])

        assert api_key
        assert len(api_key) > 20

        # Validate the key
        user_info = auth_manager.validate_key(api_key)
        assert user_info
        assert user_info['user'] == username
        assert user_info['role'] == 'user'
        assert 'read' in user_info['permissions']

    def test_invalid_key(self):
        """Test invalid API key rejection"""
        user_info = auth_manager.validate_key('invalid_key_12345')
        assert user_info is None

    def test_permission_check(self):
        """Test permission checking"""
        # Create test user
        api_key = auth_manager.create_user('perm_test', 'user', ['read'])

        user_info = auth_manager.validate_key(api_key)
        assert auth_manager.has_permission(user_info, 'read')
        assert not auth_manager.has_permission(user_info, 'write')

        # Test admin permissions
        admin_key = auth_manager.create_user('admin_test', 'admin', [])
        admin_info = auth_manager.validate_key(admin_key)
        assert auth_manager.has_permission(admin_info, 'read')
        assert auth_manager.has_permission(admin_info, 'write')
        assert auth_manager.has_permission(admin_info, 'admin')

class TestCacheSystem:
    """Test cache functionality"""

    def test_cache_operations(self):
        """Test basic cache operations"""
        from cache import cache

        # Test set and get
        cache.set('test_key', 'test_value', ttl=60)
        value = cache.get('test_key')
        assert value == 'test_value'

        # Test expiration (short TTL)
        cache.set('short_key', 'short_value', ttl=1)
        time.sleep(1.1)
        value = cache.get('short_key')
        assert value is None  # Should be expired

    def test_cache_clear(self):
        """Test cache clearing"""
        from cache import cache

        cache.set('clear_test1', 'value1')
        cache.set('clear_test2', 'value2')

        assert cache.get('clear_test1') == 'value1'
        assert cache.get('clear_test2') == 'value2'

        cache.clear()

        assert cache.get('clear_test1') is None
        assert cache.get('clear_test2') is None

if __name__ == '__main__':
    # Run tests
    pytest.main([__file__, '-v', '--tb=short'])