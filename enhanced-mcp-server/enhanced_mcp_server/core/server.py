"""Servidor MCP principal com ferramentas de IA."""

import asyncio
from typing import Any
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from enhanced_mcp_server.config import settings
from enhanced_mcp_server.tools import (
    fetch_content, search_web, translate_with_gemini, translate_with_deepl,
    ValidationError
)
from enhanced_mcp_server.prompts import (
    PROMPT_OPTIMIZATION_TEMPLATE, SIMPLE_OPTIMIZATION_TEMPLATE, TECHNICAL_PROMPT_TEMPLATE
)
from enhanced_mcp_server.utils.logging import setup_logging, get_logger

# Configura logging
setup_logging()
logger = get_logger(__name__)

# Cria servidor MCP
mcp = FastMCP(
    name="enhanced-ai-tools",
)


@mcp.tool(name="fetch", description="Busca conteúdo completo de páginas web usando Jina AI com validação de segurança")
async def fetch(url: str = Field(description="URL da página web para buscar conteúdo")) -> str:
    """Busca conteúdo de uma página web."""
    try:
        logger.info("Iniciando busca de conteúdo", url=url)
        result = await fetch_content(url)
        logger.info("Busca de conteúdo concluída com sucesso", url=url)
        return result
    except ValidationError as e:
        error_msg = f"Erro de validação: {str(e)}"
        logger.warning("Erro de validação na busca", url=url, error=error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Erro interno: {str(e)}"
        logger.error("Erro interno na busca", url=url, error=error_msg, exc_info=True)
        return error_msg


@mcp.tool(name="search", description="Pesquisa inteligente na web usando Jina AI com resultados contextualizados")
async def search(query: str = Field(description="Termo de pesquisa para buscar na web")) -> str:
    """Pesquisa na web."""
    try:
        logger.info("Iniciando pesquisa web", query=query)
        result = await search_web(query)
        logger.info("Pesquisa web concluída com sucesso", query=query)
        return result
    except ValidationError as e:
        error_msg = f"Erro de validação: {str(e)}"
        logger.warning("Erro de validação na pesquisa", query=query, error=error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Erro interno: {str(e)}"
        logger.error("Erro interno na pesquisa", query=query, error=error_msg, exc_info=True)
        return error_msg


@mcp.tool(name="translate", description="Tradução automática entre português e inglês usando Gemini AI")
async def translate(content: str = Field(description="Texto para traduzir")) -> str:
    """Traduz texto usando Gemini."""
    try:
        logger.info("Iniciando tradução com Gemini", content_length=len(content))
        result = await translate_with_gemini(content)
        logger.info("Tradução com Gemini concluída com sucesso")
        return result
    except ValidationError as e:
        error_msg = f"Erro de validação: {str(e)}"
        logger.warning("Erro de validação na tradução", error=error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Erro interno: {str(e)}"
        logger.error("Erro interno na tradução", error=error_msg, exc_info=True)
        return error_msg


@mcp.tool(name="translate_deepl", description="Tradução avançada entre múltiplos idiomas usando DeepL API")
async def translate_deepl_tool(
    content: str = Field(description="Texto para traduzir"),
    source_lang: str = Field(
        description="Idioma de origem (AR, BG, CS, DA, DE, EL, EN-GB, EN-US, ES, ET, FI, FR, HU, ID, IT, JA, KO, LT, LV, NB, NL, PL, PT-BR, PT-PT, RO, RU, SK, SL, SV, TR, UK, ZH, ZH-HANS, ZH-HANT)"
    ),
    target_lang: str = Field(
        description="Idioma de destino (AR, BG, CS, DA, DE, EL, EN-GB, EN-US, ES, ET, FI, FR, HU, ID, IT, JA, KO, LT, LV, NB, NL, PL, PT-BR, PT-PT, RO, RU, SK, SL, SV, TR, UK, ZH, ZH-HANS, ZH-HANT)"
    ),
) -> str:
    """Traduz texto usando DeepL."""
    try:
        logger.info("Iniciando tradução com DeepL",
                   content_length=len(content),
                   source_lang=source_lang,
                   target_lang=target_lang)
        result = await translate_deepl(content, source_lang, target_lang)
        logger.info("Tradução com DeepL concluída com sucesso")
        return result
    except ValidationError as e:
        error_msg = f"Erro de validação: {str(e)}"
        logger.warning("Erro de validação na tradução DeepL",
                      source_lang=source_lang,
                      target_lang=target_lang,
                      error=error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Erro interno: {str(e)}"
        logger.error("Erro interno na tradução DeepL",
                    source_lang=source_lang,
                    target_lang=target_lang,
                    error=error_msg, exc_info=True)
        return error_msg


@mcp.prompt(name="optimize_prompt", description="Otimiza prompts usando templates estruturados profissionais")
def optimize_prompt(
    content: str,
    style: str = Field(
        default="comprehensive",
        description="Estilo de otimização: comprehensive, simple, technical"
    )
) -> str:
    """Otimiza um prompt usando templates estruturados."""
    try:
        logger.info("Iniciando otimização de prompt", style=style, content_length=len(content))

        if style == "comprehensive":
            template = PROMPT_OPTIMIZATION_TEMPLATE
        elif style == "simple":
            template = SIMPLE_OPTIMIZATION_TEMPLATE
        elif style == "technical":
            template = TECHNICAL_PROMPT_TEMPLATE
        else:
            template = PROMPT_OPTIMIZATION_TEMPLATE

        optimized_prompt = f"{template}\n\n{content}"
        logger.info("Otimização de prompt concluída com sucesso", style=style)
        return optimized_prompt

    except Exception as e:
        error_msg = f"Erro na otimização do prompt: {str(e)}"
        logger.error("Erro na otimização de prompt", style=style, error=error_msg, exc_info=True)
        return error_msg


def main():
    """Função principal para executar o servidor MCP."""
    try:
        logger.info("Iniciando Enhanced MCP Server",
                   version="0.2.0",
                   jina_configured=bool(settings.jina_api_key),
                   gemini_configured=bool(settings.gemini_api_key),
                   deepl_configured=bool(settings.deepl_api_key),
                   redis_configured=bool(settings.redis_url))

        # Executa o servidor MCP
        mcp.run()

    except KeyboardInterrupt:
        logger.info("Servidor interrompido pelo usuário")
    except Exception as e:
        logger.error("Erro fatal no servidor", error=str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()