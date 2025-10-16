# Enhanced MCP Server

[![Smithery Deploy](https://img.shields.io/badge/Smithery-Publish-blue?logo=vercel)](https://smithery.ai)
[![PyPI version](https://img.shields.io/pypi/v/enhanced-mcp-server.svg)](https://pypi.org/project/enhanced-mcp-server/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Servidor MCP (Model Context Protocol) avançado e robusto que fornece ferramentas de IA para busca na web, tradução e otimização de prompts. Implementa as melhores práticas de desenvolvimento com validação de entrada, tratamento de erros abrangente, logging estruturado, cache inteligente e segurança aprimorada.

## 🚀 Funcionalidades

### Ferramentas Disponíveis
- **🔍 fetch**: Busca conteúdo completo de páginas web usando Jina AI com validação de segurança
- **🌐 search**: Pesquisa inteligente na web usando Jina AI com resultados contextualizados
- **🌍 translate_deepl**: Tradução avançada entre múltiplos idiomas usando DeepL API

### Prompts Disponíveis
- **✨ optimize_prompt**: Otimiza prompts usando templates estruturados profissionais

### Recursos Avançados
- **🧠 Cache Inteligente**: Redis com fallback para memória local
- **🔐 Sistema de Autenticação**: API keys com controle de acesso
- **📊 Interface Web**: Dashboard responsivo com tema claro/escuro
- **📝 Logging Estruturado**: Logs em JSON com níveis configuráveis
- **🛡️ Segurança Aprimorada**: Validação de entrada e rate limiting
- **🐳 Containerização**: Docker multi-stage com otimização

## 🛡️ Recursos de Segurança e Robustez

- ✅ **Validação de entrada**: URLs, consultas e textos são validados rigorosamente
- ✅ **Tratamento de erros**: Mensagens específicas e logging detalhado
- ✅ **Rate limiting**: Proteção contra abuso com configuração flexível
- ✅ **Timeouts**: Prevenção de travamentos por requests lentos
- ✅ **Sanitização**: Filtragem de termos bloqueados e URLs perigosas
- ✅ **Autenticação**: Sistema de API keys para controle de acesso
- ✅ **Auditoria**: Logs completos de todas as operações

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

### Via Smithery (Claude Desktop / clientes MCP)
```bash
npx -y @smithery/cli install @your-org/enhanced-mcp-server
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

### Verificação Local
```bash
smithery dev --key <dev-key>
```

### Checklist para Publicação
- [x] Testes passando
- [x] smithery.yaml configurado
- [x] pyproject.toml com metadados
- [x] Documentação completa
- [x] Logs estruturados
- [x] Segurança implementada

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
- [dronreef2/MCPserve](https://github.com/dronreef2/Mcpserve) - Base do projeto
- [Model Context Protocol](https://modelcontextprotocol.io/) - Protocolo MCP
- [Smithery](https://smithery.ai) - Plataforma de publicação

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/your-org/enhanced-mcp-server/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/enhanced-mcp-server/discussions)
- **Email**: team@example.com

---

**⭐ Star este repositório se achou útil!**
