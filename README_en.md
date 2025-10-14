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