# /enhanced_mcp_server/core/server.py (FastAPI MCP básico)
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="MCPserve")


@app.get("/health")
async def health() -> dict:
    """Endpoint simples para healthchecks (útil para Smithery e probes)."""
    return {"status": "ok"}

@app.post("/mcp")
async def mcp_endpoint(request: dict):
    """Endpoint MCP HTTP básico."""
    try:
        method = request.get("method")
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {
                        "tools": {
                            "listChanged": True
                        }
                    },
                    "serverInfo": {
                        "name": "MCPserve",
                        "version": "0.1.0"
                    }
                }
            }
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "tools": [
                        {
                            "name": "ping",
                            "description": "Responde com pong.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {}
                            }
                        }
                    ]
                }
            }
        elif method == "tools/call":
            tool_name = request.get("params", {}).get("name")
            if tool_name == "ping":
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": "pong"
                            }
                        ]
                    }
                }
        return JSONResponse(status_code=400, content={"error": "Method not supported"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

def create_server():
    """Retorna o app FastAPI para Smithery."""
    return app