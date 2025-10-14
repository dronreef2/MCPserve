# ai-tools MCP Server

[![Smithery Deploy](https://img.shields.io/badge/Smithery-Publish-blue?logo=vercel)](https://smithery.ai)
[![PyPI version](https://img.shields.io/pypi/v/ai-tools-mcp-server.svg)](https://pypi.org/project/ai-tools-mcp-server/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Este é um servidor MCP avançado e robusto que fornece ferramentas de IA para busca na web, tradução e otimização de prompts. Implementa as melhores práticas de desenvolvimento com validação de entrada, tratamento de erros abrangente, logging estruturado e segurança aprimorada.

## 🚀 Funcionalidades

### Ferramentas Disponíveis:
- **fetch**: Busca conteúdo de páginas web usando Jina AI (com validação de URL e segurança)
- **search**: Pesquisa na web usando Jina AI (com filtros de segurança)
- **translate**: Tradução entre idiomas usando Gemini (com validação de idiomas)
- **translate_deepl**: Tradução avançada usando DeepL API (suporte completo de idiomas)

### Prompts Disponíveis:
- **optimize_prompt**: Otimiza prompts de usuário com templates detalhados

> Nota: Este servidor é 100% stdio (não abre porta HTTP). Para ambientes de hospedagem que tentam invocar um binário `smithery`, incluímos um script shim `./smithery` que simplesmente inicia `python main.py` garantindo compatibilidade.

## 🛡️ Recursos de Segurança e Robustez

- ✅ **Validação de entrada**: URLs, consultas e textos são validados
- ✅ **Tratamento de erros**: Mensagens de erro específicas e logging detalhado
- ✅ **Rate limiting**: Proteção contra abuso das APIs
- ✅ **Timeouts**: Prevenção de travamentos por requests lentos
- ✅ **Sanitização**: Filtragem de termos bloqueados e URLs perigosas
- ✅ **Logging estruturado**: Rastreamento completo de operações
- ✅ **Configuração validada**: Verificação de chaves API no startup
- ✅ **Cache inteligente**: Redis/memory fallback para reduzir chamadas API
- ✅ **Autenticação**: Sistema de API keys para controle de acesso
- ✅ **Monitoramento**: Dashboard admin com métricas em tempo real

## 📦 Instalação

### Via PyPI (futuro publish):
```bash
pip install ai-tools-mcp-server
```

### Via Código Fonte:
```bash
git clone https://github.com/dronreef2/MCPserve.git
cd MCPserve
pip install -e .[dashboard]
```

### Via Smithery (Claude Desktop / clientes MCP):
Instalação automática:
```bash
npx -y @smithery/cli install @dronreef2/mcpserve --client claude
```

Inicialização local para desenvolvimento com túnel:
```bash
smithery dev --config smithery.config.js
```

Ou inicialização stdio (para clientes):
```bash
smithery dev --key <dev-key> --no-tunnel
```

## ⚙️ Configuração

Configure as seguintes variáveis de ambiente:

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `JINA_API_KEY` | Sim | Chave para busca e fetch via Jina AI |
| `GEMINI_API_KEY` | Não | Traduções via Gemini |
| `DEEPL_API_KEY` | Não | Traduções avançadas via DeepL |
| `REDIS_URL` | Não | URL do Redis (ex: redis://localhost:6379) |
| `LOG_LEVEL` | Não | Nível de log (INFO, DEBUG, WARNING) |
| `PORT` | Não | Porta do dashboard (default 8000) |

Exemplo rápido (.env):
```env
JINA_API_KEY=jina_xxxxxxxxx
GEMINI_API_KEY=xxxx
DEEPL_API_KEY=xxxx
REDIS_URL=redis://localhost:6379
```

## 🏃‍♂️ Execução Local

### Python (Recomendado):
```bash
python main.py
```

### Interface Web (Front-end):
```bash
# Opção 1: Script automático (recomendado)
./run_web.sh

# Opção 2: Comando direto
python web_app.py
```
Acesse: http://localhost:8001

**Recursos da Interface Web:**
- 🔍 **Buscar Conteúdo**: Interface simples para extrair conteúdo de URLs
- 🌐 **Pesquisar na Web**: Ferramenta de pesquisa com resultados formatados
- 📱 **Interface Responsiva**: Funciona em desktop e mobile
- ⚡ **Execução Direta**: Usa as ferramentas MCP diretamente (sem protocolo stdio)

### Go:
```bash
go run main.go
```

## 🧪 Testes

Execute os testes básicos:
```bash
python test_basic.py
```

### Testes de Integração E2E:
```bash
python test_e2e.py
```

### Cobertura de Testes:
- ✅ **Unidade**: Funções individuais e validações
- ✅ **Integração**: Fluxos completos de API
- ✅ **Autenticação**: Controle de acesso e permissões
- ✅ **Cache**: Operações de armazenamento/recuperação
- ✅ **E2E**: Cenários reais de uso do servidor MCP

## 📊 Monitoramento e Logs

### Dashboard Administrativo:
```bash
python dashboard.py
```
Acesse: http://localhost:8000

**Recursos do Dashboard:**
- 📈 Métricas em tempo real (CPU, memória, rede)
- 🔍 Estatísticas do cache (hits, misses, taxa de acerto)
- 👥 Gerenciamento de usuários e chaves API
- 📋 Logs de atividade do sistema
- 🏥 Status de saúde dos serviços

### Logs do Sistema:
- Logs estruturados em JSON
- Níveis configuráveis (DEBUG, INFO, WARNING, ERROR)
- Rotações automáticas de arquivos
- Monitoramento de performance e erros

O servidor gera logs estruturados com níveis apropriados:
- **INFO**: Operações normais
- **WARNING**: Problemas não críticos
- **ERROR**: Erros que requerem atenção

## 🌐 Publicação / Smithery

### Verificação local (stdio):
Se a CLI detectar `smithery.yaml`, basta:
```bash
smithery dev --key <dev-key>
```
Ou especificando manualmente o comando stdio:
```bash
smithery dev --stdio "python main.py" --key <dev-key>
```

### Publicar (após tag semver):
1. Crie tag: `git tag v0.2.0 && git push --tags`
2. Aguarde CI verde no GitHub Actions
3. O Smithery detectará automaticamente a tag e permitirá publicação via painel web (runtime Python stdio)
4. Acesse https://smithery.ai e publique o servidor

### Checklist antes do Publish:
- [x] pyproject com metadados
- [x] smithery.yaml exporta commandFunction válido
- [x] Testes passam (`pytest`)
- [x] README com instruções claras
- [x] Variáveis sensíveis não commitadas

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

- **Python**: Implementação principal com FastMCP e validações robustas
- **Go**: Versão alternativa mais performática
- **Docker**: Containerização multi-stage com configurações otimizadas
- **Configuração**: Sistema de configuração com validação
- **Logging**: Logging estruturado com níveis apropriados
- **Testes**: Suite básica de testes unitários

## ⚡ Cache e Performance

### Sistema de Cache Inteligente:
O servidor utiliza Redis para cache com fallback automático para memória:

```python
from cache import cache

@cache(ttl=3600)  # Cache por 1 hora
def expensive_api_call(query):
    # Chamada cara para API externa
    return result
```

### Benefícios do Cache:
- 🚀 **Performance**: Redução significativa no tempo de resposta
- 💰 **Custos**: Menos chamadas para APIs pagas
- 🔄 **Fallback**: Funciona mesmo sem Redis (memória local)
- 📊 **Métricas**: Estatísticas detalhadas de uso

### Configuração do Cache:
- **TTL padrão**: 1 hora para resultados de busca
- **TTL tradução**: 24 horas (conteúdo estático)
- **Limite memória**: 100MB quando sem Redis
- **Compressão**: Resultados grandes são comprimidos

## 👨‍💼 Dashboard de Administração

Interface web para monitoramento e gerenciamento:

```bash
python dashboard.py
# Acesse: http://localhost:8001
```

### Funcionalidades do Dashboard:
- 📊 **Métricas do sistema**: CPU, memória, uptime
- 📈 **Performance do cache**: Taxa de acertos, estatísticas
- 🔑 **Status das APIs**: Verificação de conectividade
- 📝 **Logs de atividade**: Ações recentes do servidor
- 🗑️ **Gerenciamento**: Limpeza de cache, reinicialização

## 🔐 Segurança e Autenticação

### Sistema de Autenticação:
O servidor implementa autenticação baseada em API keys para controle de acesso:

```python
# Gerar nova chave API
from auth import generate_api_key
key = generate_api_key("user@example.com", role="user")

# Usar chave na requisição
headers = {"Authorization": f"Bearer {key}"}
```

### Níveis de Acesso:
- **admin**: Acesso completo ao sistema e dashboard
- **user**: Acesso às ferramentas MCP
- **readonly**: Acesso apenas leitura (logs, métricas)

### Recursos de Segurança:
- 🔒 **Criptografia**: Chaves API armazenadas com hash seguro
- 🛡️ **Validação**: Todas as entradas são sanitizadas
- 🚫 **Bloqueio**: Lista de termos e URLs perigosos
- ⏱️ **Rate Limiting**: Proteção contra abuso
- 📝 **Auditoria**: Logs completos de todas as operações

## � Troubleshooting

### Problemas Comuns:

**Erro de API Key:**
```
ERROR: Missing required API key: JINA_API_KEY
```
Solução: Configure as variáveis de ambiente corretamente.

**Erro de Cache Redis:**
```
WARNING: Redis unavailable, using memory cache
```
Solução: Verifique se Redis está rodando ou configure corretamente.

**Erro de Autenticação:**
```
ERROR: Invalid API key
```
Solução: Verifique se a chave API está correta e não expirou.

### Debug Mode:
Execute com debug para mais informações:
```bash
DEBUG=1 python main.py
```

### Logs de Debug:
- Verifique `/logs/app.log` para erros detalhados
- Use o dashboard para monitorar em tempo real
- Execute testes E2E para validar funcionalidade

### Suporte:
Para suporte técnico:
1. Verifique os logs do sistema
2. Execute os testes para validar funcionamento
3. Consulte a documentação das APIs (Jina, Gemini, DeepL)
4. Abra uma issue no repositório com logs anexados

##  TODO

- [x] Implementar validação de entrada robusta
- [x] Adicionar tratamento de erros abrangente
- [x] Implementar logging estruturado
- [x] Adicionar testes básicos
- [x] Melhorar segurança das APIs
- [x] Implementar cache Redis para reduzir chamadas API
- [x] Adicionar dashboard de administração com métricas
- [x] Implementar sistema de autenticação com API keys
- [x] Criar testes E2E abrangentes
- [x] Documentar todas as funcionalidades implementadas
- [ ] Implementar métricas avançadas de performance
- [ ] Adicionar suporte a múltiplos idiomas no dashboard
- [ ] Criar documentação de API completa
- [ ] Implementar backup automático de configurações

## 🤝 Contribuição

Para contribuir:
1. Execute os testes: `python test_basic.py`
2. Verifique os logs durante desenvolvimento
3. Adicione testes para novas funcionalidades
4. Siga as melhores práticas de segurança implementadas
5. Use o smithery-ai[bot] para assistência no desenvolvimento

## 📄 Licença

MIT License - veja LICENSE para detalhes.
