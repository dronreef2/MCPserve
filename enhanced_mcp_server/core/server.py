# /enhanced_mcp_server/core/server.py (FastMCP configurado para HTTP)
import os
from mcp.server.fastmcp import FastMCP

def create_server():
    """Cria um servidor MCP HTTP com ferramentas básicas."""
    mcp = FastMCP(
        name="enhanced-mcp-server",
        streamable_http_path="/mcp",  # Endpoint MCP HTTP
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )

    @mcp.tool(name="ping", description="Responde com pong.")
    async def ping() -> str:
        return "pong"

    return mcp.app  # Retorna o app FastAPI configurado para HTTP
