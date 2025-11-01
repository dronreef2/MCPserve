# MCPserve

[![Smithery Deploy](https://img.shields.io/badge/Smithery-Publish-blue?logo=vercel)](https://smithery.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![smithery badge](https://smithery.ai/badge/@dronreef2/MCPserve)](https://smithery.ai/server/@dronreef2/MCPserve)

Servidor MCP (Model Context Protocol) básico implementado em Python com FastAPI. Fornece ferramentas de IA para busca na web, tradução e otimização de prompts através do protocolo MCP HTTP.

## 🚀 Funcionalidades

### Ferramentas Disponíveis
- **🏓 ping**: Ferramenta básica que responde "pong" (implementada)
- **🔍 fetch**: Busca conteúdo completo de páginas web usando Jina AI (planejado)
- **🌐 search**: Pesquisa inteligente na web usando Jina AI (planejado)
- **🌍 translate_deepl**: Tradução avançada entre múltiplos idiomas usando DeepL API (planejado)

### Recursos Avançados
- **📡 Protocolo MCP HTTP**: Implementação completa do Model Context Protocol via HTTP
- **🐳 Containerização**: Docker com Python 3.12 e uv para gerenciamento de dependências
- **� Configuração**: Sistema de configurações com Pydantic e variáveis de ambiente
- **📝 Logging Estruturado**: Logs estruturados com structlog
- **🗄️ Cache**: Sistema de cache com Redis (opcional) e fallback para memória

## �️ Status do Projeto

### ✅ Implementado
- Servidor MCP HTTP básico funcional
- Endpoint `/mcp` com suporte aos métodos: `initialize`, `tools/list`, `tools/call`
- Ferramenta `ping` funcional
- Deploy automático no Smithery
- Configuração com API keys (Jina, DeepL)
- Sistema de cache inteligente
- Containerização com Docker

### � Em Desenvolvimento
- Implementação das ferramentas completas (fetch, search, translate)
- Interface web de monitoramento
- Sistema de autenticação
- Rate limiting e segurança avançada

### 📋 Próximos Passos
1. Implementar ferramenta `fetch` para busca de conteúdo web
2. Implementar ferramenta `search` para pesquisa na web
3. Implementar ferramenta `translate_deepl` para tradução
4. Adicionar interface web de dashboard
5. Implementar sistema de autenticação e rate limiting
6. Adicionar testes automatizados
7. Documentação completa das APIs

## 📦 Instalação

### Via PyPI (futuro)
```bash
pip install enhanced-mcp-server
```

### Via Código Fonte
```bash
git clone https://github.com/your-org/enhanced-mcp-server.git
cd enhanced-mcp-server
pip install -e .[web,cache]
```

## 📦 Instalação

### Via Smithery (Recomendado)
```bash
npx -y @smithery/cli install @dronreef2/MCPserve --client claude
```

### Via Código Fonte
```bash
git clone https://github.com/dronreef2/MCPserve.git
cd MCPserve
pip install -e .
```

### Docker
```bash
# Construir e executar
docker-compose up --build

# Apenas o servidor MCP
docker run mcpserve python -m enhanced_mcp_server.main
```

## ⚙️ Configuração

Configure as variáveis de ambiente no arquivo `.env`:

```env
# API Keys (obrigatórias para funcionalidades específicas)
JINA_API_KEY=jina_your_api_key_here
DEEPL_API_KEY=your_deepl_api_key_here

# Cache (opcional)
REDIS_URL=redis://localhost:6379

# Logging
LOG_LEVEL=INFO

# Web Interface
WEB_HOST=0.0.0.0
WEB_PORT=8001

# Segurança
ENABLE_AUTH=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60
```

## 🏃‍♂️ Execução

### Modo MCP (stdio)
```bash
# Verificar configuração
python -m enhanced_mcp_server.main --check-config

# Executar servidor MCP
python -m enhanced_mcp_server.main
```

### Interface Web
```bash
# Executar aplicação web
python -m enhanced_mcp_server.web.app

# Ou usar o script direto
enhanced-mcp-web
```
Acesse: http://localhost:8001

### Docker
```bash
# Construir e executar
docker-compose up --build

# Apenas o servidor MCP
docker run enhanced-mcp-server python -m enhanced_mcp_server.main
```

## 🧪 Testes

```bash
# Todos os testes
pytest

# Testes específicos
pytest tests/test_tools.py
pytest tests/test_cache.py
pytest tests/test_auth.py

# Com cobertura
pytest --cov=enhanced_mcp_server --cov-report=html
```

## 📊 Monitoramento

### Interface Web
- **Dashboard**: http://localhost:8001
- **Health Check**: http://localhost:8001/health
- **Cache Stats**: http://localhost:8001/cache/stats

### Logs
```bash
# Visualizar logs em tempo real
tail -f logs/app.log

# Logs estruturados (JSON)
jq . logs/app.log
```

## 🏗️ Arquitetura

```
enhanced-mcp-server/
├── enhanced_mcp_server/
│   ├── core/           # Servidor MCP principal
│   ├── tools/          # Implementação das ferramentas
│   ├── prompts/        # Templates de otimização
│   ├── cache/          # Sistema de cache inteligente
│   ├── auth/           # Autenticação e autorização
│   ├── config/         # Configurações centralizadas
│   ├── utils/          # Utilitários (logging, etc.)
│   └── web/            # Interface web FastAPI
├── tests/              # Testes unitários e integração
├── templates/          # Templates HTML
├── static/             # Arquivos estáticos
└── docs/               # Documentação
```

## ⚡ Cache e Performance

### Sistema de Cache Híbrido
- **Redis**: Cache distribuído de alta performance
- **Memória**: Fallback automático quando Redis indisponível
- **TTL Inteligente**: Tempos de vida diferentes por tipo de conteúdo
- **Compressão**: Resultados grandes são comprimidos automaticamente

### Configuração de Cache
```python
# Cache automático com decorador
@cache.cached(ttl=3600)
async def expensive_operation():
    return await api_call()
```

## 🔐 Segurança e Autenticação

### Sistema de API Keys
```python
from enhanced_mcp_server.auth import auth_manager

# Gerar nova chave
key = auth_manager.generate_api_key("user@example.com", role="user")

# Validar chave
user = auth_manager.validate_api_key(api_key)
```

### Níveis de Acesso
- **admin**: Acesso completo ao sistema
- **user**: Acesso às ferramentas MCP
- **readonly**: Acesso apenas leitura

## 🌐 Publicação / Smithery

### Deploy Automático
O projeto é automaticamente implantado no Smithery a partir de pushes na branch `main`. O deploy usa o `smithery.yaml` e a função factory `enhanced_mcp_server.core.server:create_server`.

### Verificação Local
```bash
# Instalar Smithery CLI
npm install -g @smithery/cli

# Verificar configuração local
smithery inspect @dronreef2/MCPserve

# Executar servidor localmente para testes
smithery run @dronreef2/MCPserve --config '{"JINA_API_KEY":"your_key","DEEPL_API_KEY":"your_key"}'

# Abrir playground para testes interativos
smithery playground --key your_smithery_key
```

### Instruções de Deploy Manual (se necessário)
1. **Configure Secrets no Smithery**:
   - `JINA_API_KEY`: Chave da API Jina AI (obrigatória para ferramentas de busca)
   - `DEEPL_API_KEY`: Chave da API DeepL (obrigatória para tradução)
   - `REDIS_URL`: URL do Redis (opcional, usa cache em memória se não definido)

2. **Configure Environment Variables**:
   - `WEB_PORT`: Porta do servidor (padrão: 8001)
   - `LOG_LEVEL`: Nível de logging (INFO, DEBUG, etc.)

3. **Health Checks**:
   - Configure liveness probe: `GET /health`
   - Configure readiness probe: `GET /health`

4. **Recursos**:
   - Memória recomendada: 512Mi
   - CPU: 0.5 vCPU
   - Porta exposta: 8001 (TCP)

### Checklist para Publicação
- [x] smithery.yaml configurado com server factory
- [x] pyproject.toml com [tool.smithery] server
- [x] Dockerfile multi-stage para build otimizado
- [x] Endpoint /health para probes
- [x] Secrets configurados (JINA_API_KEY, DEEPL_API_KEY)
- [x] Testes básicos passando
- [x] Logs estruturados habilitados

### Desenvolvimento com Smithery CLI
```bash
# Iniciar servidor de desenvolvimento com hot-reload (usa smithery.config.js)
smithery dev --port 8001 --key your_dev_key

# Construir para produção
smithery build --out dist/server.cjs --transport shttp

# Testar instalação local
smithery install @dronreef2/MCPserve --client claude --config '{"JINA_API_KEY":"test_key"}'
```

**Nota**: O arquivo `smithery.config.js` está configurado para desenvolvimento local com o Smithery CLI, permitindo hot-reload e testes integrados.

## 🧪 Teste das Ferramentas

### Exemplos de Uso
```python
# Buscar conteúdo web
result = await fetch("https://example.com")

# Pesquisar na web
results = await search("tecnologia MCP")

# Traduzir texto
translation = await translate("Hello world", "en", "pt")

# Otimizar prompt
optimized = optimize_prompt("Como criar um servidor MCP?")
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit suas mudanças: `git commit -am 'Adiciona nova funcionalidade'`
4. Push para a branch: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

### Diretrizes
- Siga PEP 8 para código Python
- Adicione testes para novas funcionalidades
- Atualize a documentação
- Use commits semânticos

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [yiGmMk/mcp-server](https://github.com/yiGmMk/mcp-server) - Inspiração inicial
- [dronreef2/MCPserve](https://github.com/dronreef2/MCPserve) - Base do projeto
- [Model Context Protocol](https://modelcontextprotocol.io/) - Protocolo MCP
- [Smithery](https://smithery.ai) - Plataforma de publicação

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/your-org/enhanced-mcp-server/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/enhanced-mcp-server/discussions)
- **Email**: team@example.com

---

**⭐ Star este repositório se achou útil!**
