# ai-tools MCP Server

Este é um servidor MCP avançado que fornece ferramentas de IA para busca na web, tradução e otimização de prompts. Suporta implementações em Python e Go com deployment via Docker e Smithery.

## 🚀 Funcionalidades

### Ferramentas Disponíveis:
- **fetch**: Busca conteúdo de páginas web usando Jina AI
- **search**: Pesquisa na web usando Jina AI
- **translate**: Tradução entre idiomas usando Gemini
- **translate_deepl**: Tradução avançada usando DeepL API

### Prompts Disponíveis:
- **optimize_prompt**: Otimiza prompts de usuário com templates detalhados

## 📦 Instalação

1. Clone o repositório
2. Instale dependências Python:
   ```bash
   pip install -e .
   ```
3. Configure as chaves de API (veja Configuração)

## ⚙️ Configuração

Configure as seguintes variáveis de ambiente:
- `JINA_API_KEY`: Chave da API Jina AI (obrigatória)
- `GEMINI_API_KEY`: Chave da API Gemini (opcional, para tradução)
- `DEEPL_API_KEY`: Chave da API DeepL (opcional, para tradução avançada)

## 🏃‍♂️ Execução Local

### Python (Recomendado):
```bash
python main.py
```

### Go:
```bash
go run main.go
```

### Docker:
```bash
docker-compose up go-app  # ou python-app
```

## 🌐 Deployment com Smithery

O projeto está configurado para deployment automático no Smithery:

```bash
smithery deploy
```

Isso permitirá que o smithery-ai[bot] tenha acesso ao servidor MCP.

## 🧪 Teste das Ferramentas

### Exemplo de uso das ferramentas:
```python
# Buscar conteúdo de uma página
fetch("https://example.com")

# Pesquisar na web
search("tecnologia MCP")

# Traduzir texto
translate("Olá mundo", "pt", "en")

# Otimizar prompt
optimize_prompt("Como criar um servidor MCP?")
```

## 🏗️ Arquitetura

- **Python**: Implementação principal com FastMCP
- **Go**: Versão alternativa com mcp-go
- **Docker**: Containerização multi-stage
- **Smithery**: Plataforma de deployment e descoberta

## 📝 TODO

- Resolver deployment Python no Smithery (serviço sai imediatamente)
- Implementar tradução completa no Go
- Adicionar mais ferramentas de IA
- Melhorar tratamento de erros

## 🤝 Contribuição

Para contribuir, você pode:
1. Abrir issues para bugs ou sugestões
2. Criar pull requests
3. Usar o smithery-ai[bot] para assistência no desenvolvimento

## 📄 Licença

MIT License - veja LICENSE para detalhes.
