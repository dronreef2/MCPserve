#!/usr/bin/env python3
"""
Web Frontend for AI Tools MCP Server
Provides a simple web interface to use fetch and search tools.
"""

import os
import logging
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

# Import our MCP server functions
from main import handle_call_tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AI Tools Web Interface", description="Web interface for MCP server tools")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Create templates directory if it doesn't exist
os.makedirs("templates", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with tool selection"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/fetch", response_class=HTMLResponse)
async def fetch_form(request: Request):
    """Fetch tool form"""
    return templates.TemplateResponse("fetch.html", {"request": request})

@app.post("/fetch", response_class=HTMLResponse)
async def fetch_url(request: Request, url: str = Form(...)):
    """Execute fetch tool"""
    try:
        # Call our MCP tool directly
        result = await handle_call_tool("fetch", {"url": url})

        # Extract text content
        content = result[0].text if result else "No content returned"

        return templates.TemplateResponse("fetch.html", {
            "request": request,
            "url": url,
            "result": content,
            "success": True
        })
    except Exception as e:
        logger.error(f"Fetch error: {e}")
        return templates.TemplateResponse("fetch.html", {
            "request": request,
            "url": url,
            "error": str(e),
            "success": False
        })

@app.get("/search", response_class=HTMLResponse)
async def search_form(request: Request):
    """Search tool form"""
    return templates.TemplateResponse("search.html", {"request": request})

@app.post("/search", response_class=HTMLResponse)
async def search_query(request: Request, query: str = Form(...)):
    """Execute search tool"""
    try:
        # Call our MCP tool directly
        result = await handle_call_tool("search", {"query": query})

        # Extract text content
        content = result[0].text if result else "No results returned"

        return templates.TemplateResponse("search.html", {
            "request": request,
            "query": query,
            "result": content,
            "success": True
        })
    except Exception as e:
        logger.error(f"Search error: {e}")
        return templates.TemplateResponse("search.html", {
            "request": request,
            "query": query,
            "error": str(e),
            "success": False
        })

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "tools": ["fetch", "search"]}

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()

    port = int(os.getenv("WEB_PORT", "8001"))
    logger.info(f"Starting web interface on port {port}")

    uvicorn.run(app, host="0.0.0.0", port=port)