# /Dockerfile (versão corrigida)

FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instala ferramentas de build do Python
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copia os arquivos de configuração e instala o pacote em modo editável
# Isso permite que o `python -m` funcione corretamente
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir -e .

# Copia o resto do código da aplicação
COPY enhanced_mcp_server ./enhanced_mcp_server

# Expõe a porta que o servidor HTTP vai usar
# A Smithery vai mapear uma porta externa para esta
EXPOSE 8001

# Comando para iniciar o servidor. Use `python -m` para executar o pacote.
CMD ["python", "-m", "enhanced_mcp_server.main"]