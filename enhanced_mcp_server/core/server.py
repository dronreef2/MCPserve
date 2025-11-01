# /enhanced_mcp_server/core/server.py (FastAPI MCP básico)
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from enhanced_mcp_server.tools import fetch_content, search_web, translate_with_deepl

app = FastAPI(title="MCPserve")


@app.get("/health")
async def health() -> dict:
    """Endpoint simples para healthchecks (útil para Smithery e probes)."""
    return {"status": "ok"}

@app.get("/.well-known/mcp-config")
async def well_known_mcp_config() -> dict:
    """Configuração padrão para clientes MCP."""
    return {
        "mcpServers": {
            "default": {
                "transport": {
                    "type": "http",
                    "endpoint": "/mcp"
                },
                "authentication": {
                    "type": "none"
                }
            }
        }
    }


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
                            },
                            "annotations": {
                                "readOnlyHint": True,
                                "destructiveHint": False,
                                "idempotentHint": True
                            }
                        },
                        {
                            "name": "fetch",
                            "description": "Busca conteúdo completo de uma página web usando Jina AI.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "url": {
                                        "type": "string",
                                        "description": "URL da página web a ser buscada"
                                    }
                                },
                                "required": ["url"]
                            },
                            "annotations": {
                                "readOnlyHint": True,
                                "destructiveHint": False,
                                "idempotentHint": True
                            }
                        },
                        {
                            "name": "search",
                            "description": "Pesquisa na web usando Jina AI e retorna resultados estruturados.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {
                                        "type": "string",
                                        "description": "Termo de pesquisa"
                                    }
                                },
                                "required": ["query"]
                            },
                            "annotations": {
                                "readOnlyHint": True,
                                "destructiveHint": False,
                                "idempotentHint": True
                            }
                        }
                    ]
                }
            }
        elif method == "tools/call":
            tool_name = request.get("params", {}).get("name")
            tool_args = request.get("params", {}).get("arguments", {})
            
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
            elif tool_name == "fetch":
                url = tool_args.get("url")
                if not url:
                    raise HTTPException(status_code=400, detail="URL parameter required")
                try:
                    result = await fetch_content(url)
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": result
                                }
                            ]
                        }
                    }
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Fetch failed: {str(e)}")
            elif tool_name == "search":
                query = tool_args.get("query")
                if not query:
                    raise HTTPException(status_code=400, detail="Query parameter required")
                try:
                    result = await search_web(query)
                    return {
                        "jsonrpc": "2.0",
                        "id": request.get("id"),
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": result
                                }
                            ]
                        }
                    }
                except Exception as e:
                    raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
        raise HTTPException(status_code=400, detail="Method not supported")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_server():
    """Retorna o app FastAPI para Smithery."""
    return app