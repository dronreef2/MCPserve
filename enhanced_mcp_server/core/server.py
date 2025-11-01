# /enhanced_mcp_server/core/server.py (FastAPI MCP básico)
import os
from typing import Mapping

from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.base import BaseHTTPMiddleware
from enhanced_mcp_server.tools import translate_with_deepl
from enhanced_mcp_server.utils.logging import get_logger

prefix_from_env = os.environ.get("SMITHERY_PREFIX", "").rstrip("/")

app = FastAPI(title="MCPserve", root_path=prefix_from_env)
logger = get_logger(__name__)


class SmitheryPrefixMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        prefix = request.headers.get("x-smithery-prefix") or prefix_from_env
        if prefix:
            cleaned = prefix.rstrip("/")
            scope = request.scope
            if cleaned:
                scope["root_path"] = cleaned
                path: str = scope.get("path", "")
                if path.startswith(cleaned):
                    trimmed = path[len(cleaned):] or "/"
                    scope["path"] = trimmed
        return await call_next(request)


app.add_middleware(SmitheryPrefixMiddleware)


SESSION_CONFIG_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "$id": "https://server.smithery.ai/@dronreef2/mcpserve/.well-known/mcp-config",
    "title": "Configuração de Sessão do MCPserve",
    "description": "Parâmetros opcionais para personalizar o comportamento do MCPserve por sessão.",
    "x-query-style": "dot",
    "type": "object",
    "properties": {
        "deeplApiKey": {
            "type": "string",
            "title": "DeepL API Key",
            "description": "Chave de API para habilitar a ferramenta de tradução."
        },
        "redisUrl": {
            "type": "string",
            "title": "Redis URL",
            "description": "Endpoint Redis para cache compartilhado (opcional)."
        },
        "logLevel": {
            "type": "string",
            "title": "Log Level",
            "description": "Nível de log desejado para a sessão.",
            "default": "INFO",
            "enum": ["DEBUG", "INFO", "WARNING", "ERROR"]
        },
        "enableAuth": {
            "type": "boolean",
            "title": "Ativar autenticação",
            "description": "Indica se endpoints sensíveis exigem autenticação.",
            "default": False
        }
    },
    "required": [],
    "additionalProperties": False
}


def _parse_bool(value: str) -> bool:
    return value.lower() in {"1", "true", "t", "yes", "y"}


def _parse_session_config(query_params: Mapping[str, str]) -> dict:
    """Converte parâmetros da query string em configuração de sessão."""
    config: dict[str, object] = {}

    if "deeplApiKey" in query_params:
        config["deepl_api_key"] = query_params["deeplApiKey"]
    if "redisUrl" in query_params:
        config["redis_url"] = query_params["redisUrl"]
    if "logLevel" in query_params:
        config["log_level"] = query_params["logLevel"]
    if "enableAuth" in query_params:
        config["enable_auth"] = _parse_bool(query_params["enableAuth"])

    return config


@app.get("/health")
async def health() -> dict:
    """Endpoint simples para healthchecks (útil para Smithery e probes)."""
    return {"status": "ok"}

@app.get("/.well-known/mcp-config")
async def well_known_mcp_config() -> dict:
    """Retorna metadados MCP para auto-descoberta e configuração."""
    return {
        "mcpServers": {
            "default": {
                "transport": {
                    "type": "http",
                    "endpoint": f"{prefix_from_env}/mcp" if prefix_from_env else "/mcp"
                },
                "authentication": {
                    "type": "none"
                }
            }
        },
        "sessionConfigSchema": SESSION_CONFIG_SCHEMA
    }


@app.post("/mcp")
async def mcp_endpoint(request: Request):
    """Endpoint MCP HTTP básico."""
    try:
        payload = await request.json()
        method = payload.get("method")
        session_config = _parse_session_config(request.query_params)
        logger.debug("MCP request recebido", method=method)

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": payload.get("id"),
                "result": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {
                        "tools": {
                            "listChanged": True
                        },
                        "sessionConfigSchema": SESSION_CONFIG_SCHEMA
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
                "id": payload.get("id"),
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
                        }
                    ]
                }
            }
        elif method == "tools/call":
            params = payload.get("params", {})
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})

            if tool_name == "ping":
                return {
                    "jsonrpc": "2.0",
                    "id": payload.get("id"),
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": "pong"
                            }
                        ]
                    }
                }
        elif method in {"ping", "heartbeat/ping"}:
            return {
                "jsonrpc": "2.0",
                "id": payload.get("id"),
                "result": {"pong": True}
            }
        raise HTTPException(status_code=400, detail="Method not supported")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def create_server():
    """Retorna o app FastAPI para Smithery."""
    return app