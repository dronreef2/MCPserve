#!/usr/bin/env python3
"""Ponto de entrada principal do Enhanced MCP Server."""

import argparse
import asyncio
from enhanced_mcp_server.utils.logging import setup_logging, get_logger
from enhanced_mcp_server.config import settings

logger = get_logger(__name__)


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(description="Enhanced MCP Server")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default=settings.log_level,
        help="Nível de logging"
    )
    parser.add_argument(
        "--check-config",
        action="store_true",
        help="Verifica configuração e sai"
    )
    parser.add_argument(
        "--http",
        action="store_true",
        help="Executa servidor HTTP (para desenvolvimento)"
    )

    args = parser.parse_args()

    # Atualiza configuração de logging se especificada
    if args.log_level != settings.log_level:
        settings.log_level = args.log_level

    # Configura logging
    setup_logging()

    # Verifica configuração se solicitado
    if args.check_config:
        print("🔍 Verificando configuração...")
        print(f"  JINA_API_KEY: {'✅ Configurada' if settings.jina_api_key else '❌ Não configurada'}")
        print(f"  DEEPL_API_KEY: {'✅ Configurada' if settings.deepl_api_key else '❌ Não configurada'}")
        print(f"  REDIS_URL: {'✅ Configurada' if settings.redis_url else '⚠️  Usando cache em memória'}")
        print(f"  Log Level: {settings.log_level}")
        print("✅ Verificação concluída")
        return

    # Executa o servidor
    if args.http:
        # Modo HTTP para desenvolvimento local
        import uvicorn
        from enhanced_mcp_server.core.server import app
        logger.info("Starting HTTP server", host=settings.web_host, port=settings.web_port)
        uvicorn.run(app, host=settings.web_host, port=settings.web_port)
    else:
        # Modo stdio para MCP (padrão)
        logger.info("Starting MCP server in stdio mode")
        print("MCP Server running in stdio mode. Use --http for HTTP mode.", flush=True)
        # Para stdio mode, o servidor FastAPI é exposto via create_server() para Smithery
        # Em modo local, mostramos apenas uma mensagem
        print("For Smithery deployment, the server is exposed via create_server().", flush=True)


if __name__ == "__main__":
    main()