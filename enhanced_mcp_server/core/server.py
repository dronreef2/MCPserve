# /enhanced_mcp_server/core/server.py (FastMCP HTTP simplificado)
import os
from mcp.server.fastmcp import FastMCP

def create_server():
    """Cria um servidor MCP HTTP simplificado."""
    # Configuração mais simples para compatibilidade
    mcp = FastMCP(name="MCPserve")

    @mcp.tool(name="ping", description="Responde com pong.")
    async def ping() -> str:
        return "pong"

    # Retornar o app HTTP diretamente
    return mcp.streamable_http_app()