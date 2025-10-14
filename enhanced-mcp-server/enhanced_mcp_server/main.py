#!/usr/bin/env python3
"""Ponto de entrada principal do Enhanced MCP Server."""

import sys
import argparse
from enhanced_mcp_server.core.server import main as server_main
from enhanced_mcp_server.utils.logging import setup_logging
from enhanced_mcp_server.config import settings


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
        print(f"  GEMINI_API_KEY: {'✅ Configurada' if settings.gemini_api_key else '❌ Não configurada'}")
        print(f"  DEEPL_API_KEY: {'✅ Configurada' if settings.deepl_api_key else '❌ Não configurada'}")
        print(f"  REDIS_URL: {'✅ Configurada' if settings.redis_url else '⚠️  Usando cache em memória'}")
        print(f"  Log Level: {settings.log_level}")
        print("✅ Verificação concluída")
        return

    # Executa o servidor
    server_main()


if __name__ == "__main__":
    main()