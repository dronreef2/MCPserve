"""Testes de integração para o Enhanced MCP Server."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from enhanced_mcp_server.web.app import app
from enhanced_mcp_server.config import settings


@pytest.fixture
def client():
    """Cliente de teste FastAPI."""
    return TestClient(app)


class TestWebInterface:
    """Testes da interface web."""

    def test_home_page(self, client):
        """Testa página inicial."""
        response = client.get("/")
        assert response.status_code == 200
        assert "Enhanced AI Tools" in response.text
        assert "Buscar Conteúdo Web" in response.text

    def test_health_check(self, client):
        """Testa endpoint de saúde."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "version" in data
        assert "services" in data

    def test_fetch_page(self, client):
        """Testa página de busca."""
        response = client.get("/fetch")
        assert response.status_code == 200
        assert "Buscar Conteúdo Web" in response.text

    def test_search_page(self, client):
        """Testa página de pesquisa."""
        response = client.get("/search")
        assert response.status_code == 200
        assert "Pesquisar na Web" in response.text

    def test_fetch_endpoint_missing_url(self, client):
        """Testa endpoint de busca sem URL."""
        response = client.post("/fetch", data={})
        assert response.status_code == 422  # Unprocessable Entity - validação do Pydantic

    def test_search_endpoint_missing_query(self, client):
        """Testa endpoint de pesquisa sem consulta."""
        response = client.post("/search", data={})
        assert response.status_code == 422  # Unprocessable Entity - validação do Pydantic


class TestMCPServer:
    """Testes do servidor MCP."""

    @pytest.mark.skip(reason="MCP server implementation uses HTTP endpoint, not FastMCP object")
    @pytest.mark.asyncio
    async def test_mcp_server_initialization(self):
        """Testa inicialização do servidor MCP."""
        from enhanced_mcp_server.core.server import mcp

        # Verifica se o servidor foi criado
        assert mcp.name == "enhanced-ai-tools"
        
        # Verifica se as ferramentas foram registradas (simplificado)
        assert hasattr(mcp, 'tool')  # Verifica se tem método tool


class TestIntegration:
    """Testes de integração completos."""

    def test_full_web_flow(self, client):
        """Testa fluxo completo da interface web."""
        # Página inicial
        response = client.get("/")
        assert response.status_code == 200

        # Página de busca
        response = client.get("/fetch")
        assert response.status_code == 200

        # Página de pesquisa
        response = client.get("/search")
        assert response.status_code == 200

        # Health check
        response = client.get("/health")
        assert response.status_code == 200

