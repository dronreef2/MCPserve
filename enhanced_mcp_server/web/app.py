"""Aplicação web FastAPI para interface das ferramentas MCP."""

import os
from typing import Optional
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from enhanced_mcp_server.config import settings
from enhanced_mcp_server.tools import (
    fetch_content, search_web, ValidationError
)
from enhanced_mcp_server.utils.logging import setup_logging, get_logger
from enhanced_mcp_server.cache import cache

# Configura logging
setup_logging()
logger = get_logger(__name__)

# Cria aplicação FastAPI
app = FastAPI(
    title="Enhanced AI Tools",
    description="Interface web para ferramentas de IA avançadas",
    version="0.2.0"
)

# Configura templates e arquivos estáticos
if os.path.exists("templates"):
    templates = Jinja2Templates(directory="templates")
else:
    templates = None
    
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


class FetchRequest(BaseModel):
    url: str


class SearchRequest(BaseModel):
    query: str


class TranslateRequest(BaseModel):
    content: str
    source_lang: Optional[str] = "auto"
    target_lang: Optional[str] = "auto"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Página inicial."""
    if templates is None:
        return HTMLResponse(
            "<html><body><h1>Enhanced MCP Server</h1>"
            "<p>Web interface not available. Templates directory not found.</p>"
            "<p>Use the MCP API endpoints at <code>/mcp</code></p>"
            "</body></html>"
        )
    return templates.TemplateResponse("index.html", {
        "request": request,
        "tools": [
            {
                "name": "fetch",
                "title": "Buscar Conteúdo Web",
                "description": "Extraia conteúdo completo de qualquer página web",
                "icon": "fas fa-search",
                "color": "primary"
            },
            {
                "name": "search",
                "title": "Pesquisar na Web",
                "description": "Realize buscas inteligentes na web usando IA",
                "icon": "fas fa-search-plus",
                "color": "secondary"
            },
            {
                "name": "translate",
                "title": "Tradução Gemini",
                "description": "Traduza entre português e inglês com Gemini",
                "icon": "fas fa-language",
                "color": "success"
            },
            {
                "name": "translate_deepl",
                "title": "Tradução DeepL",
                "description": "Tradução avançada entre múltiplos idiomas",
                "icon": "fas fa-globe",
                "color": "info"
            }
        ]
    })


@app.get("/fetch", response_class=HTMLResponse)
async def fetch_page(request: Request):
    """Página de busca de conteúdo."""
    if templates is None:
        return HTMLResponse("<html><body><h1>Templates not available</h1></body></html>")
    return templates.TemplateResponse("fetch.html", {"request": request})


@app.post("/fetch")
async def fetch_endpoint(url: str = Form(...)):
    """Endpoint para busca de conteúdo."""
    try:
        logger.info("Requisição de busca de conteúdo", url=url)
        result = await fetch_content(url)
        return {"success": True, "result": result}
    except ValidationError as e:
        logger.warning("Erro de validação na busca web", url=url, error=str(e))
        return {"success": False, "result": f"Erro de validação: {str(e)}"}
    except Exception as e:
        logger.error("Erro interno na busca web", url=url, error=str(e), exc_info=True)
        return {"success": False, "result": f"Erro interno: {str(e)}"}


@app.get("/search", response_class=HTMLResponse)
async def search_page(request: Request):
    """Página de pesquisa web."""
    if templates is None:
        return HTMLResponse("<html><body><h1>Templates not available</h1></body></html>")
    return templates.TemplateResponse("search.html", {"request": request})


@app.post("/search")
async def search_endpoint(query: str = Form(...)):
    """Endpoint para pesquisa web."""
    try:
        logger.info("Requisição de pesquisa web", query=query)
        result = await search_web(query)
        return {"success": True, "result": result}
    except ValidationError as e:
        logger.warning("Erro de validação na pesquisa", query=query, error=str(e))
        return {"success": False, "result": f"Erro de validação: {str(e)}"}
    except Exception as e:
        logger.error("Erro interno na pesquisa", query=query, error=str(e), exc_info=True)
        return {"success": False, "result": f"Erro interno: {str(e)}"}


@app.get("/health")
async def health_check():
    """Endpoint de verificação de saúde."""
    return {
        "status": "healthy",
        "version": "0.2.0",
        "services": {
            "jina": bool(settings.jina_api_key),
            "gemini": bool(settings.gemini_api_key),
            "deepl": bool(settings.deepl_api_key),
            "redis": bool(settings.redis_url)
        }
    }


@app.get("/cache/stats")
async def cache_stats():
    """Estatísticas do cache."""
    # Esta é uma implementação simplificada
    # Em produção, você poderia expor métricas mais detalhadas
    return {
        "cache_type": "redis" if settings.redis_url else "memory",
        "configured": bool(settings.redis_url or cache._memory_cache)
    }


def main():
    """Função principal para executar a aplicação web."""
    import uvicorn

    logger.info("Iniciando aplicação web",
               host=settings.web_host,
               port=settings.web_port,
               reload=settings.web_reload)

    uvicorn.run(
        "enhanced_mcp_server.web.app:app",
        host=settings.web_host,
        port=settings.web_port,
        reload=settings.web_reload,
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    main()