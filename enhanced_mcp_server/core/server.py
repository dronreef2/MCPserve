# /enhanced_mcp_server/core/server.py (versão de teste MÍNIMA)
from mcp.server.fastmcp import FastMCP
from smithery.decorators import smithery

# NÃO importe nada mais do seu projeto.
# NÃO configure logging aqui.

@smithery.server()
def create_server():
    """Cria um servidor MCP mínimo para teste de deploy."""
    mcp = FastMCP(name="test-server")

    @mcp.tool(name="ping", description="Responde com pong.")
    async def ping() -> str:
        return "pong"
        
    return mcp
