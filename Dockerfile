# Multi-stage build para imagem final mais leve
FROM python:3.11-slim as builder

WORKDIR /app

# Instala dependências do sistema para build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instala ferramentas de build do Python
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copia os arquivos de configuração e o código da aplicação
COPY pyproject.toml README.md ./
COPY enhanced_mcp_server ./enhanced_mcp_server

# Instala o pacote em modo editável
RUN pip install --no-cache-dir -e .

# Stage de runtime (imagem final leve)
FROM python:3.11-slim as runtime

WORKDIR /app

# Copia pacotes instalados e código da aplicação do stage builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app/enhanced_mcp_server /app/enhanced_mcp_server
COPY --from=builder /app/pyproject.toml /app/README.md /app/

# Expõe a porta que o servidor HTTP vai usar
EXPOSE 8001

# Comando para iniciar o servidor HTTP
CMD ["python", "-m", "enhanced_mcp_server.main", "--http"]