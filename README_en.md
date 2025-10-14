# ai-tools MCP Server

This is an advanced MCP server providing AI tools for web fetching, search, translation, and prompt optimization. Supports Python and Go implementations with Docker deployment and Smithery integration.

## 🚀 Features

### Available Tools:
- **fetch**: Fetch web page content using Jina AI
- **search**: Search the web using Jina AI
- **translate**: Translate between languages using Gemini
- **translate_deepl**: Advanced translation using DeepL API

### Available Prompts:
- **optimize_prompt**: Optimize user prompts with detailed templates

## 📦 Installation

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -e .
   ```
3. Configure API keys (see Configuration)

## ⚙️ Configuration

Set the following environment variables:
- `JINA_API_KEY`: Jina AI API key (required)
- `GEMINI_API_KEY`: Gemini API key (optional, for translation)
- `DEEPL_API_KEY`: DeepL API key (optional, for advanced translation)

## 🏃‍♂️ Running Locally

### Python (Recommended):
```bash
python main.py
```

### Go:
```bash
go run main.go
```

### Docker:
```bash
docker-compose up go-app  # or python-app
```

## 🌐 Smithery Deployment

The project is configured for automatic deployment on Smithery:

```bash
smithery deploy
```

This will allow the smithery-ai[bot] to access the MCP server.

## 🧪 Tool Testing

### Tool usage examples:
```python
# Fetch page content
fetch("https://example.com")

# Search the web
search("MCP technology")

# Translate text
translate("Hello world", "en", "pt")

# Optimize prompt
optimize_prompt("How to create an MCP server?")
```

## 🏗️ Architecture

- **Python**: Main implementation with FastMCP
- **Go**: Alternative version with mcp-go
- **Docker**: Multi-stage containerization
- **Smithery**: Deployment and discovery platform

## 📝 TODO

- Fix Python Docker deployment on Smithery (service exits immediately)
- Implement full translation in Go
- Add more AI tools
- Improve error handling

## 🤝 Contributing

To contribute, you can:
1. Open issues for bugs or suggestions
2. Create pull requests
3. Use smithery-ai[bot] for development assistance

## 📄 License

MIT License - see LICENSE for details.

New API KeySMITHERY v1.5.2 Building MCP server with streamable http transport...
Press Ctrl+C to stop the server
✓ Initial build complete
$ node .smithery/index.cjs
> Server starting on port 8081
> Injecting cors middleware
✗ Failed to start MCP server: Error: No valid server export found. Please export:
- export default function({ sessionId, config }) { ... } (stateful)
- export default function({ config }) { ... } (stateless)
    at startMcpServer (/workspaces/MCPserve/.smithery/index.cjs:87873:13)
    at Object.<anonymous> (/workspaces/MCPserve/.smithery/index.cjs:87883:1)
    at Module._compile (node:internal/modules/cjs/loader:1730:14)
    at Object..js (node:internal/modules/cjs/loader:1895:10)
    at Module.load (node:internal/modules/cjs/loader:1465:32)
    at Function._load (node:internal/modules/cjs/loader:1282:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:235:24)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:171:5)
    at node:internal/main/run_main_module:36:49
⚠️  Process exited with code 1

o/ Shutting down server...

  SMITHERY v1.5.2 ready

  ➜  Local:      http://localhost:8081/
  ➜  Remote:     https://accb7d3a.ngrok.smithery.ai
  ➜  Playground: https://smithery.ai/playground?mcp=https%3A%2F%2Faccb7d3a.ngrok.smithery.ai%2Fmcp

  ╭ Add to Client ──────────────────────────────────────────────────────────────────────╮
  │ Cursor: cursor://anysphere.cursor-deeplink/mcp/install?name=smithery-dev&config=... │
  │ VS Code: vscode:mcp/install?{"name":"smithery-dev","type":"http",...}               │
  │                                                                                     │
  │ Note: If required config needed, attach using URL params                            │
  │ e.g. https://server.com/mcp?weatherApiKey=abc123                                    │
  ╰─────────────────────────────────────────────────────────────────────────────────────╯

Could not open browser automatically
Please open the link manually
SMITHERY v1.5.2 Building MCP server with streamable http transport...
Press Ctrl+C to stop the server
✓ Initial build complete
$ node .smithery/index.cjs
> Server starting on port 8081
> Injecting cors middleware
✗ Failed to start MCP server: Error: No valid server export found. Please export:
- export default function({ sessionId, config }) { ... } (stateful)
- export default function({ config }) { ... } (stateless)
    at startMcpServer (/workspaces/MCPserve/.smithery/index.cjs:87873:13)
    at Object.<anonymous> (/workspaces/MCPserve/.smithery/index.cjs:87883:1)
    at Module._compile (node:internal/modules/cjs/loader:1730:14)
    at Object..js (node:internal/modules/cjs/loader:1895:10)
    at Module.load (node:internal/modules/cjs/loader:1465:32)
    at Function._load (node:internal/modules/cjs/loader:1282:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:235:24)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:171:5)
    at node:internal/main/run_main_module:36:49
⚠️  Process exited with code 1

o/ Shutting down server...

  SMITHERY v1.5.2 ready

  ➜  Local:      http://localhost:8081/
  ➜  Remote:     https://accb7d3a.ngrok.smithery.ai
  ➜  Playground: https://smithery.ai/playground?mcp=https%3A%2F%2Faccb7d3a.ngrok.smithery.ai%2Fmcp

  ╭ Add to Client ──────────────────────────────────────────────────────────────────────╮
  │ Cursor: cursor://anysphere.cursor-deeplink/mcp/install?name=smithery-dev&config=... │
  │ VS Code: vscode:mcp/install?{"name":"smithery-dev","type":"http",...}               │
  │                                                                                     │
  │ Note: If required config needed, attach using URL params                            │
  │ e.g. https://server.com/mcp?weatherApiKey=abc123                                    │
  ╰─────────────────────────────────────────────────────────────────────────────────────╯

Could not open browser automatically
Please open the link manually
SMITHERY v1.5.2 Building MCP server with streamable http transport...
Press Ctrl+C to stop the server
✓ Initial build complete
$ node .smithery/index.cjs
> Server starting on port 8081
> Injecting cors middleware
✗ Failed to start MCP server: Error: No valid server export found. Please export:
- export default function({ sessionId, config }) { ... } (stateful)
- export default function({ config }) { ... } (stateless)
    at startMcpServer (/workspaces/MCPserve/.smithery/index.cjs:87873:13)
    at Object.<anonymous> (/workspaces/MCPserve/.smithery/index.cjs:87883:1)
    at Module._compile (node:internal/modules/cjs/loader:1730:14)
    at Object..js (node:internal/modules/cjs/loader:1895:10)
    at Module.load (node:internal/modules/cjs/loader:1465:32)
    at Function._load (node:internal/modules/cjs/loader:1282:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:235:24)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:171:5)
    at node:internal/main/run_main_module:36:49
⚠️  Process exited with code 1

o/ Shutting down server...

  SMITHERY v1.5.2 ready

  ➜  Local:      http://localhost:8081/
  ➜  Remote:     https://accb7d3a.ngrok.smithery.ai
  ➜  Playground: https://smithery.ai/playground?mcp=https%3A%2F%2Faccb7d3a.ngrok.smithery.ai%2Fmcp

  ╭ Add to Client ──────────────────────────────────────────────────────────────────────╮
  │ Cursor: cursor://anysphere.cursor-deeplink/mcp/install?name=smithery-dev&config=... │
  │ VS Code: vscode:mcp/install?{"name":"smithery-dev","type":"http",...}               │
  │                                                                                     │
  │ Note: If required config needed, attach using URL params                            │
  │ e.g. https://server.com/mcp?weatherApiKey=abc123                                    │
  ╰─────────────────────────────────────────────────────────────────────────────────────╯

Could not open browser automatically
Please open the link manually
SMITHERY v1.5.2 Building MCP server with streamable http transport...
Press Ctrl+C to stop the server
✓ Initial build complete
$ node .smithery/index.cjs
> Server starting on port 8081
> Injecting cors middleware
✗ Failed to start MCP server: Error: No valid server export found. Please export:
- export default function({ sessionId, config }) { ... } (stateful)
- export default function({ config }) { ... } (stateless)
    at startMcpServer (/workspaces/MCPserve/.smithery/index.cjs:87873:13)
    at Object.<anonymous> (/workspaces/MCPserve/.smithery/index.cjs:87883:1)
    at Module._compile (node:internal/modules/cjs/loader:1730:14)
    at Object..js (node:internal/modules/cjs/loader:1895:10)
    at Module.load (node:internal/modules/cjs/loader:1465:32)
    at Function._load (node:internal/modules/cjs/loader:1282:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:235:24)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:171:5)
    at node:internal/main/run_main_module:36:49
⚠️  Process exited with code 1

o/ Shutting down server...

  SMITHERY v1.5.2 ready

  ➜  Local:      http://localhost:8081/
  ➜  Remote:     https://accb7d3a.ngrok.smithery.ai
  ➜  Playground: https://smithery.ai/playground?mcp=https%3A%2F%2Faccb7d3a.ngrok.smithery.ai%2Fmcp

  ╭ Add to Client ──────────────────────────────────────────────────────────────────────╮
  │ Cursor: cursor://anysphere.cursor-deeplink/mcp/install?name=smithery-dev&config=... │
  │ VS Code: vscode:mcp/install?{"name":"smithery-dev","type":"http",...}               │
  │                                                                                     │
  │ Note: If required config needed, attach using URL params                            │
  │ e.g. https://server.com/mcp?weatherApiKey=abc123                                    │
  ╰─────────────────────────────────────────────────────────────────────────────────────╯

Could not open browser automatically
Please open the link manually
SMITHERY v1.5.2 Building MCP server with streamable http transport...
Press Ctrl+C to stop the server
✓ Initial build complete
$ node .smithery/index.cjs
> Server starting on port 8081
> Injecting cors middleware
✗ Failed to start MCP server: Error: No valid server export found. Please export:
- export default function({ sessionId, config }) { ... } (stateful)
- export default function({ config }) { ... } (stateless)
    at startMcpServer (/workspaces/MCPserve/.smithery/index.cjs:87873:13)
    at Object.<anonymous> (/workspaces/MCPserve/.smithery/index.cjs:87883:1)
    at Module._compile (node:internal/modules/cjs/loader:1730:14)
    at Object..js (node:internal/modules/cjs/loader:1895:10)
    at Module.load (node:internal/modules/cjs/loader:1465:32)
    at Function._load (node:internal/modules/cjs/loader:1282:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:235:24)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:171:5)
    at node:internal/main/run_main_module:36:49
⚠️  Process exited with code 1

o/ Shutting down server...

  SMITHERY v1.5.2 ready

  ➜  Local:      http://localhost:8081/
  ➜  Remote:     https://accb7d3a.ngrok.smithery.ai
  ➜  Playground: https://smithery.ai/playground?mcp=https%3A%2F%2Faccb7d3a.ngrok.smithery.ai%2Fmcp

  ╭ Add to Client ──────────────────────────────────────────────────────────────────────╮
  │ Cursor: cursor://anysphere.cursor-deeplink/mcp/install?name=smithery-dev&config=... │
  │ VS Code: vscode:mcp/install?{"name":"smithery-dev","type":"http",...}               │
  │                                                                                     │
  │ Note: If required config needed, attach using URL params                            │
  │ e.g. https://server.com/mcp?weatherApiKey=abc123                                    │
  ╰─────────────────────────────────────────────────────────────────────────────────────╯

SMITHERY v1.5.2 Building MCP server with streamable http transport...
Press Ctrl+C to stop the server
✓ Initial build complete
$ node .smithery/index.cjs
> Server starting on port 8081
> Injecting cors middleware
✗ Failed to start MCP server: Error: No valid server export found. Please export:
- export default function({ sessionId, config }) { ... } (stateful)
- export default function({ config }) { ... } (stateless)
    at startMcpServer (/workspaces/MCPserve/.smithery/index.cjs:87873:13)
    at Object.<anonymous> (/workspaces/MCPserve/.smithery/index.cjs:87883:1)
    at Module._compile (node:internal/modules/cjs/loader:1730:14)
    at Object..js (node:internal/modules/cjs/loader:1895:10)
    at Module.load (node:internal/modules/cjs/loader:1465:32)
    at Function._load (node:internal/modules/cjs/loader:1282:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:235:24)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:171:5)
    at node:internal/main/run_main_module:36:49
⚠️  Process exited with code 1

o/ Shutting down server...

  SMITHERY v1.5.2 ready

  ➜  Local:      http://localhost:8081/
  ➜  Remote:     https://accb7d3a.ngrok.smithery.ai
  ➜  Playground: https://smithery.ai/playground?mcp=https%3A%2F%2Faccb7d3a.ngrok.smithery.ai%2Fmcp

  ╭ Add to Client ──────────────────────────────────────────────────────────────────────╮
  │ Cursor: cursor://anysphere.cursor-deeplink/mcp/install?name=smithery-dev&config=... │
  │ VS Code: vscode:mcp/install?{"name":"smithery-dev","type":"http",...}               │
  │                                                                                     │
  │ Note: If required config needed, attach using URL params                            │
  │ e.g. https://server.com/mcp?weatherApiKey=abc123                                    │
  ╰─────────────────────────────────────────────────────────────────────────────────────╯

Could not open browser automatically
Please open the link manually
SMITHERY v1.5.2 Building MCP server with streamable http transport...
Press Ctrl+C to stop the server
✓ Initial build complete
$ node .smithery/index.cjs
> Server starting on port 8081
> Injecting cors middleware
✗ Failed to start MCP server: Error: No valid server export found. Please export:
- export default function({ sessionId, config }) { ... } (stateful)
- export default function({ config }) { ... } (stateless)
    at startMcpServer (/workspaces/MCPserve/.smithery/index.cjs:87873:13)
    at Object.<anonymous> (/workspaces/MCPserve/.smithery/index.cjs:87883:1)
    at Module._compile (node:internal/modules/cjs/loader:1730:14)
    at Object..js (node:internal/modules/cjs/loader:1895:10)
    at Module.load (node:internal/modules/cjs/loader:1465:32)
    at Function._load (node:internal/modules/cjs/loader:1282:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:235:24)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:171:5)
    at node:internal/main/run_main_module:36:49
⚠️  Process exited with code 1

o/ Shutting down server...

  SMITHERY v1.5.2 ready

  ➜  Local:      http://localhost:8081/
  ➜  Remote:     https://accb7d3a.ngrok.smithery.ai
  ➜  Playground: https://smithery.ai/playground?mcp=https%3A%2F%2Faccb7d3a.ngrok.smithery.ai%2Fmcp

  ╭ Add to Client ──────────────────────────────────────────────────────────────────────╮
  │ Cursor: cursor://anysphere.cursor-deeplink/mcp/install?name=smithery-dev&config=... │
  │ VS Code: vscode:mcp/install?{"name":"smithery-dev","type":"http",...}               │
  │                                                                                     │
  │ Note: If required config needed, attach using URL params                            │
  │ e.g. https://server.com/mcp?weatherApiKey=abc123                                    │
  ╰─────────────────────────────────────────────────────────────────────────────────────╯

Could not open browser automatically
Please open the link manually
SMITHERY v1.5.2 Building MCP server with streamable http transport...
Press Ctrl+C to stop the server
✓ Initial build complete
$ node .smithery/index.cjs
> Server starting on port 8081
> Injecting cors middleware
✗ Failed to start MCP server: Error: No valid server export found. Please export:
- export default function({ sessionId, config }) { ... } (stateful)
- export default function({ config }) { ... } (stateless)
    at startMcpServer (/workspaces/MCPserve/.smithery/index.cjs:87873:13)
    at Object.<anonymous> (/workspaces/MCPserve/.smithery/index.cjs:87883:1)
    at Module._compile (node:internal/modules/cjs/loader:1730:14)
    at Object..js (node:internal/modules/cjs/loader:1895:10)
    at Module.load (node:internal/modules/cjs/loader:1465:32)
    at Function._load (node:internal/modules/cjs/loader:1282:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:235:24)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:171:5)
    at node:internal/main/run_main_module:36:49
⚠️  Process exited with code 1

o/ Shutting down server...

  SMITHERY v1.5.2 ready

  ➜  Local:      http://localhost:8081/
  ➜  Remote:     https://accb7d3a.ngrok.smithery.ai
  ➜  Playground: https://smithery.ai/playground?mcp=https%3A%2F%2Faccb7d3a.ngrok.smithery.ai%2Fmcp

  ╭ Add to Client ──────────────────────────────────────────────────────────────────────╮
  │ Cursor: cursor://anysphere.cursor-deeplink/mcp/install?name=smithery-dev&config=... │
  │ VS Code: vscode:mcp/install?{"name":"smithery-dev","type":"http",...}               │
  │                                                                                     │
  │ Note: If required config needed, attach using URL params                            │
  │ e.g. https://server.com/mcp?weatherApiKey=abc123                                    │
  ╰─────────────────────────────────────────────────────────────────────────────────────╯

Could not open browser automatically
Please open the link manually
SMITHERY v1.5.2 Building MCP server with streamable http transport...
Press Ctrl+C to stop the server
✓ Initial build complete
$ node .smithery/index.cjs
> Server starting on port 8081
> Injecting cors middleware
✗ Failed to start MCP server: Error: No valid server export found. Please export:
- export default function({ sessionId, config }) { ... } (stateful)
- export default function({ config }) { ... } (stateless)
    at startMcpServer (/workspaces/MCPserve/.smithery/index.cjs:87873:13)
    at Object.<anonymous> (/workspaces/MCPserve/.smithery/index.cjs:87883:1)
    at Module._compile (node:internal/modules/cjs/loader:1730:14)
    at Object..js (node:internal/modules/cjs/loader:1895:10)
    at Module.load (node:internal/modules/cjs/loader:1465:32)
    at Function._load (node:internal/modules/cjs/loader:1282:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:235:24)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:171:5)
    at node:internal/main/run_main_module:36:49
⚠️  Process exited with code 1

o/ Shutting down server...

  SMITHERY v1.5.2 ready

  ➜  Local:      http://localhost:8081/
  ➜  Remote:     https://accb7d3a.ngrok.smithery.ai
  ➜  Playground: https://smithery.ai/playground?mcp=https%3A%2F%2Faccb7d3a.ngrok.smithery.ai%2Fmcp

  ╭ Add to Client ──────────────────────────────────────────────────────────────────────╮
  │ Cursor: cursor://anysphere.cursor-deeplink/mcp/install?name=smithery-dev&config=... │
  │ VS Code: vscode:mcp/install?{"name":"smithery-dev","type":"http",...}               │
  │                                                                                     │
  │ Note: If required config needed, attach using URL params                            │
  │ e.g. https://server.com/mcp?weatherApiKey=abc123                                    │
  ╰─────────────────────────────────────────────────────────────────────────────────────╯

Could not open browser automatically
Please open the link manually
SMITHERY v1.5.2 Building MCP server with streamable http transport...
Press Ctrl+C to stop the server
✓ Initial build complete
$ node .smithery/index.cjs
> Server starting on port 8081
> Injecting cors middleware
✗ Failed to start MCP server: Error: No valid server export found. Please export:
- export default function({ sessionId, config }) { ... } (stateful)
- export default function({ config }) { ... } (stateless)
    at startMcpServer (/workspaces/MCPserve/.smithery/index.cjs:87873:13)
    at Object.<anonymous> (/workspaces/MCPserve/.smithery/index.cjs:87883:1)
    at Module._compile (node:internal/modules/cjs/loader:1730:14)
    at Object..js (node:internal/modules/cjs/loader:1895:10)
    at Module.load (node:internal/modules/cjs/loader:1465:32)
    at Function._load (node:internal/modules/cjs/loader:1282:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:235:24)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:171:5)
    at node:internal/main/run_main_module:36:49
⚠️  Process exited with code 1

o/ Shutting down server...

  SMITHERY v1.5.2 ready

  ➜  Local:      http://localhost:8081/
  ➜  Remote:     https://accb7d3a.ngrok.smithery.ai
  ➜  Playground: https://smithery.ai/playground?mcp=https%3A%2F%2Faccb7d3a.ngrok.smithery.ai%2Fmcp

  ╭ Add to Client ──────────────────────────────────────────────────────────────────────╮
  │ Cursor: cursor://anysphere.cursor-deeplink/mcp/install?name=smithery-dev&config=... │
  │ VS Code: vscode:mcp/install?{"name":"smithery-dev","type":"http",...}               │
  │                                                                                     │
  │ Note: If required config needed, attach using URL params                            │
  │ e.g. https://server.com/mcp?weatherApiKey=abc123                                    │
  ╰─────────────────────────────────────────────────────────────────────────────────────╯

Could not open browser automatically
Please open the link manually
