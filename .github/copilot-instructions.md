# MCPserve - AI Agent Instructions

## Architecture Overview
This is a Python MCP (Model Context Protocol) server built with FastAPI, providing AI tools for web search, translation, and prompt optimization. Currently implements basic MCP HTTP protocol with a ping tool, with plans for full tool implementation.

## Current Implementation Status

### ✅ Completed
- **Basic MCP HTTP Server**: FastAPI-based server implementing MCP protocol
- **Ping Tool**: Simple tool that responds with "pong"
- **Smithery Deployment**: Automatic deployment with Docker and uv
- **Configuration System**: Pydantic settings with environment variables
- **Caching System**: Redis lazy loading with memory fallback
- **Structured Logging**: JSON logging with configurable levels

### 🚧 In Progress / Planned
- **Full Tool Implementation**: fetch, search, translate_deepl tools
- **Web Dashboard**: Monitoring interface
- **Authentication System**: API key management
- **Rate Limiting**: Request throttling
- **Comprehensive Testing**: Unit and integration tests

## Key Components

- **Core Server** (`enhanced_mcp_server/core/server.py`): FastAPI MCP server with HTTP endpoints
- **Cache** (`enhanced_mcp_server/cache/`): Redis with lazy connection + memory fallback
- **Config** (`enhanced_mcp_server/config/settings.py`): Pydantic settings with `.env` support
- **Utils** (`enhanced_mcp_server/utils/`): Structured logging with `structlog`

## Critical Patterns & Conventions

### MCP HTTP Protocol Implementation
```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="MCPserve")

@app.post("/mcp")
async def mcp_endpoint(request: dict):
    """Handle MCP protocol requests."""
    method = request.get("method")
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "protocolVersion": "2025-06-18",
                "capabilities": {"tools": {"listChanged": True}},
                "serverInfo": {"name": "MCPserve", "version": "0.1.0"}
            }
        }
    # Handle other methods...
```

### Configuration Access
```python
from enhanced_mcp_server.config import settings

# Access settings (auto-loaded from .env)
api_key = settings.jina_api_key
timeout = settings.request_timeout
```

### Logging
```python
from enhanced_mcp_server.utils.logging import get_logger

logger = get_logger(__name__)
logger.info("Operation completed", user_id=user.id, duration=1.2)
```

### Caching
```python
from enhanced_mcp_server.cache import cached

@cached(ttl=3600)  # Cache for 1 hour
async def expensive_api_call(query: str):
    return await api_request(query)
```

## Development Workflows

### Local Development
```bash
# Check configuration
python -m enhanced_mcp_server.main --check-config

# Run MCP server (stdio mode)
python -m enhanced_mcp_server.main

# Test MCP server with smithery CLI
smithery inspect @dronreef2/MCPserve
```

### Docker Development
```bash
# Full stack with docker-compose
docker-compose up --build

# Just MCP server
docker run mcpserve python -m enhanced_mcp_server.main
```

### Testing
```bash
# All tests
pytest

# With coverage
pytest --cov=enhanced_mcp_server --cov-report=html
```

### Smithery Deployment
- Automatic deployment from `main` branch pushes
- Server function: `enhanced_mcp_server.core.server:create_server`
- Returns FastAPI app for HTTP MCP protocol
- Configuration in `smithery.yaml` (minimal) + `[tool.smithery]` in `pyproject.toml`

## Key Implementation Notes

### Redis Lazy Loading
Redis connection is established only on first cache access, preventing startup delays. Never call Redis operations during module import.

### Security-First Approach
- All URLs validated against dangerous patterns (localhost, private IPs)
- API keys required for external services
- Rate limiting and input sanitization
- Structured audit logging

### Portuguese Documentation
Code comments and documentation are in Portuguese. Maintain this convention for consistency.

### Environment Variables
Critical settings loaded from `.env`:
- `JINA_API_KEY`, `DEEPL_API_KEY` (required for tools)
- `REDIS_URL` (optional, falls back to memory cache)
- `LOG_LEVEL`, `LOG_FORMAT` (json/console)

### Tool Registration
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="enhanced-mcp-server")

@mcp.tool(name="tool_name", description="Tool description")
async def tool_function(param: str) -> dict:
    # Implementation
    return result
```

## File Structure Reference
- `enhanced_mcp_server/core/`: Server implementation (FastAPI MCP server)
- `enhanced_mcp_server/tools/`: MCP tool definitions (currently basic ping)
- `enhanced_mcp_server/cache/`: Caching system with Redis fallback
- `enhanced_mcp_server/config/`: Settings management with Pydantic
- `enhanced_mcp_server/utils/`: Logging and utilities
- `tests/`: Pytest test suite (to be implemented)
- `templates/`: HTML templates (planned)
- `static/`: Static web assets (planned)</content>
<parameter name="filePath">/workspaces/MCPserve/.github/copilot-instructions.md