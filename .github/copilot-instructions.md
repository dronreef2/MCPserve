# Enhanced MCP Server - AI Agent Instructions

## Architecture Overview
This is a Python MCP (Model Context Protocol) server built with FastMCP, providing AI tools for web search, translation, and prompt optimization. Key components:

- **Core Server** (`enhanced_mcp_server/core/server.py`): FastMCP instance with HTTP deployment
- **Tools** (`enhanced_mcp_server/tools/`): Web fetch, search, translation, and prompt optimization
- **Cache** (`enhanced_mcp_server/cache/`): Redis with lazy connection + memory fallback
- **Auth** (`enhanced_mcp_server/auth/`): API key-based authentication system
- **Config** (`enhanced_mcp_server/config/settings.py`): Pydantic settings with `.env` support
- **Web** (`enhanced_mcp_server/web/`): FastAPI dashboard for monitoring
- **Utils** (`enhanced_mcp_server/utils/`): Structured logging with `structlog`

## Critical Patterns & Conventions

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

### URL Validation
```python
from enhanced_mcp_server.tools import validate_url

if not validate_url(url):
    raise ValidationError("Invalid or unsafe URL")
```

### Error Handling
```python
from enhanced_mcp_server.tools import ValidationError

try:
    result = await operation()
except ValidationError as e:
    logger.warning("Validation failed", error=str(e))
    return {"error": "Invalid input"}
```

## Development Workflows

### Local Development
```bash
# Check configuration
python -m enhanced_mcp_server.main --check-config

# Run MCP server (stdio mode)
python -m enhanced_mcp_server.main

# Run web interface
python -m enhanced_mcp_server.web.app
```

### Docker Development
```bash
# Full stack with docker-compose
docker-compose up --build

# Just MCP server
docker run enhanced-mcp-server python -m enhanced_mcp_server.main
```

### Testing
```bash
# All tests
pytest

# With coverage
pytest --cov=enhanced_mcp_server --cov-report=html

# Specific test file
pytest tests/test_tools.py
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
- `enhanced_mcp_server/core/`: Server implementation
- `enhanced_mcp_server/tools/`: MCP tool definitions
- `enhanced_mcp_server/cache/`: Caching system
- `enhanced_mcp_server/auth/`: Authentication
- `enhanced_mcp_server/config/`: Settings management
- `enhanced_mcp_server/web/`: Web dashboard
- `enhanced_mcp_server/utils/`: Logging and utilities
- `tests/`: Pytest test suite
- `templates/`: HTML templates
- `static/`: Static web assets</content>
<parameter name="filePath">/workspaces/MCPserve/.github/copilot-instructions.md