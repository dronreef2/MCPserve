# /enhanced_mcp_server/core/server.py (versão SEM decorator smithery)
from mcp.server.fastmcp import FastMCP

def create_server():
    """Cria um servidor MCP mínimo SEM decorator smithery."""
    mcp = FastMCP(name="test-server")
    
    @mcp.tool(name="ping", description="Responde com pong.")
    async def ping() -> str:
        return "pong"
        
    return mcp
