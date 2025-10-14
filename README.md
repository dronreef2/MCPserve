# MCPserve

An MCP (Model Context Protocol) Server implementation supporting both Python and Go.

## Setup

### Environment Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and configure the required variables:
   - `MCP_SERVER_HOST`: Server host (default: localhost)
   - `MCP_SERVER_PORT`: Server port (default: 8000)
   - `MCP_SERVER_ENV`: Environment (development/production)
   - Add API keys if needed for integrations (OpenAI, Anthropic, etc.)

### Environment Variables

The `.env.example` file includes configurations for:
- Server settings (host, port, environment)
- API integrations (OpenAI, Anthropic)
- Database connections (PostgreSQL, Redis)
- Logging configuration
- Security settings
- Feature flags
- CORS settings
- Rate limiting
- Timeout settings

## Development

Make sure to never commit your `.env` file to version control. It's already included in `.gitignore`.

## Usage

Configure your environment variables in the `.env` file according to your deployment needs.