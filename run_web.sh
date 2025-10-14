#!/bin/bash
# Script para executar a interface web

echo "🚀 Iniciando interface web do AI Tools MCP Server..."
echo "📱 Acesse: http://localhost:8001"
echo ""

# Carregar variáveis de ambiente se existir .env
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
    echo "✅ Variáveis de ambiente carregadas do .env"
fi

# Verificar se as dependências estão instaladas
python -c "import fastapi, uvicorn, jinja2" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Instalando dependências web..."
    pip install fastapi uvicorn jinja2
fi

# Executar a aplicação web
python web_app.py