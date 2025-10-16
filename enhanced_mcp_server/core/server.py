# /enhanced_mcp_server/core/server.py (versão restaurada com HTTP)
import os
import uvicorn
from mcp.server.fastmcp import FastMCP

def create_server():
    """Cria um servidor MCP com ferramentas básicas."""
    mcp = FastMCP(name="enhanced-mcp-server")
    
    @mcp.tool(name="ping", description="Responde com pong.")
    async def ping() -> str:
        return "pong"
        
    return mcp

def main():
    """Executa o servidor HTTP."""
    server = create_server()
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(server.app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
