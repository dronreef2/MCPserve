# /enhanced_mcp_server/core/server.py (retorna FastAPI app para Smithery)
import os
from mcp.server.fastmcp import FastMCP

def create_server():
    """Cria um servidor MCP com ferramentas básicas e retorna o app FastAPI."""
    mcp = FastMCP(name="enhanced-mcp-server")
    
    @mcp.tool(name="ping", description="Responde com pong.")
    async def ping() -> str:
        return "pong"
        
    return mcp.app  # Retorna o app FastAPI para Smithery gerenciar
