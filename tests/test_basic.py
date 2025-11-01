"""Testes básicos para o Enhanced MCP Server."""

import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient
from enhanced_mcp_server.tools import (
    translate_with_deepl,
    ValidationError, validate_url, validate_language_code
)
from enhanced_mcp_server.cache import cache
from enhanced_mcp_server.config import settings
from enhanced_mcp_server.core.server import app


class TestValidation:
    """Testes de validação."""

    def test_validate_url_valid(self):
        """Testa URLs válidas."""
        assert validate_url("https://example.com")
        assert validate_url("http://test.com/path")
        assert validate_url("https://sub.domain.com/path?query=value")

    def test_validate_url_invalid(self):
        """Testa URLs inválidas."""
        assert not validate_url("not-a-url")
        assert not validate_url("ftp://example.com")
        assert not validate_url("http://localhost:3000")  # localhost bloqueado
        assert not validate_url("https://127.0.0.1")  # IP local bloqueado

    def test_validate_language_code(self):
        """Testa códigos de idioma."""
        assert validate_language_code("PT-BR")
        assert validate_language_code("en")
        assert validate_language_code("ZH")
        assert not validate_language_code("INVALID")
        assert not validate_language_code("")


class TestCache:
    """Testes do sistema de cache."""

    def test_cache_get_set(self):
        """Testa operações básicas de cache."""
        # Limpa cache de memória para teste
        cache._memory_cache.clear()

        # Testa cache vazio
        assert cache.get("nonexistent") is None

        # Testa set e get
        cache.set("test_key", "test_value", ttl=60)
        assert cache.get("test_key") == "test_value"

    def test_cache_expiration(self):
        """Testa expiração de cache."""
        cache._memory_cache.clear()

        # Cache com TTL muito curto
        cache.set("expire_key", "value", ttl=0.001)
        import time
        time.sleep(0.01)  # Espera expiração

        assert cache.get("expire_key") is None


class TestConfig:
    """Testes de configuração."""

    def test_settings_defaults(self):
        """Testa valores padrão das configurações."""
        assert settings.web_port == 8001
        assert settings.log_level == "INFO"
        assert settings.cache_ttl == 3600
        assert settings.enable_auth is True

    def test_settings_env_override(self):
        """Testa override de configurações via ambiente."""
        with patch.dict('os.environ', {'WEB_PORT': '9000', 'LOG_LEVEL': 'DEBUG'}):
            from enhanced_mcp_server.config.settings import Settings
            test_settings = Settings()
            assert test_settings.web_port == 9000
            assert test_settings.log_level == "DEBUG"


class TestServer:
    """Testes do servidor FastAPI."""

    def test_health_endpoint(self):
        """Testa endpoint de health check."""
        client = TestClient(app)
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    def test_create_server_factory(self):
        """Testa função factory create_server."""
        from enhanced_mcp_server.core.server import create_server
        server_app = create_server()
        assert server_app is app  # Deve retornar a mesma instância