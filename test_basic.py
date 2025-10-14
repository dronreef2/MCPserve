#!/usr/bin/env python3
"""
Basic tests for MCP Server functionality
Run with: python test_basic.py
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import Config
from gpt import call_gemini

class TestConfig(unittest.TestCase):
    """Test configuration validation"""

    def test_missing_required_env(self):
        """Test that missing required env vars raise ValueError"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                Config()

    def test_valid_config(self):
        """Test valid configuration"""
        env_vars = {
            'JINA_API_KEY': 'jina_test_key_123',
            'GEMINI_API_KEY': 'test_gemini_key',
            'DEEPL_API_KEY': 'test_deepl_key'
        }
        with patch.dict(os.environ, env_vars):
            config = Config()
            self.assertEqual(config.jina_api_key, 'jina_test_key_123')
            self.assertEqual(config.gemini_api_key, 'test_gemini_key')
            self.assertEqual(config.deepl_api_key, 'test_deepl_key')

class TestGeminiAPI(unittest.TestCase):
    """Test Gemini API calls"""

    @patch('gpt.OpenAI')
    def test_call_gemini_success(self, mock_openai):
        """Test successful Gemini API call"""
        # Mock the response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"

        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            result = call_gemini("Test prompt")
            self.assertEqual(result, "Test response")

    def test_call_gemini_missing_key(self):
        """Test Gemini API call with missing key"""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                call_gemini("Test prompt")

class TestInputValidation(unittest.TestCase):
    """Test input validation functions"""

    def test_url_validation(self):
        """Test URL format validation"""
        from urllib.parse import urlparse

        valid_urls = [
            "https://example.com",
            "http://test.com/path",
            "https://sub.example.com/path?query=value"
        ]

        invalid_urls = [
            "not-a-url",
            "ftp://example.com",  # FTP not allowed
            "",
            "example.com",  # missing scheme
            "http://",  # incomplete
            "https://",  # incomplete
        ]

        for url in valid_urls:
            parsed = urlparse(url)
            self.assertTrue(parsed.scheme and parsed.netloc, f"URL should be valid: {url}")

        for url in invalid_urls:
            parsed = urlparse(url)
            # Invalid if missing scheme, netloc, or using unsupported scheme
            is_invalid = not parsed.scheme or not parsed.netloc or parsed.scheme not in ['http', 'https']
            self.assertTrue(is_invalid, f"URL should be invalid: {url}")

if __name__ == '__main__':
    # Set up test environment
    os.environ.setdefault('JINA_API_KEY', 'test_jina_key')
    os.environ.setdefault('GEMINI_API_KEY', 'test_gemini_key')
    os.environ.setdefault('DEEPL_API_KEY', 'test_deepl_key')

    # Run tests
    unittest.main(verbosity=2)