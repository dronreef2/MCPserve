#!/usr/bin/env python3
"""
AI Tools MCP Server - Standard MCP Implementation
Provides web fetching, search, and translation tools via Jina AI, Gemini, and DeepL APIs.
"""

import os
import logging
import asyncio
import json
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
import requests

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    GetPromptRequest,
    ListPromptsRequest,
    Prompt,
    PromptMessage,
    PromptArgument
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
JINA_API_KEY = os.getenv("JINA_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

if not JINA_API_KEY:
    logger.error("JINA_API_KEY environment variable is required")
    exit(1)

# Create server instance
server = Server("ai-tools")

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """List available tools"""
    tools = [
        Tool(
            name="fetch",
            description="Fetch content from a web page using Jina AI Reader",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to fetch content from"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="search",
            description="Search the web using Jina AI Search",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string", 
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="translate",
            description="Translate text using Gemini AI (requires GEMINI_API_KEY)",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to translate"
                    },
                    "target_language": {
                        "type": "string",
                        "description": "Target language (e.g., 'Portuguese', 'Spanish', 'French')"
                    },
                    "source_language": {
                        "type": "string",
                        "description": "Source language (optional, auto-detect if not provided)"
                    }
                },
                "required": ["text", "target_language"]
            }
        ),
        Tool(
            name="translate_deepl",
            description="Advanced translation using DeepL API (requires DEEPL_API_KEY)",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to translate"
                    },
                    "target_language": {
                        "type": "string",
                        "description": "Target language code (e.g., 'PT', 'ES', 'FR', 'DE')"
                    },
                    "source_language": {
                        "type": "string", 
                        "description": "Source language code (optional, auto-detect if not provided)"
                    }
                },
                "required": ["text", "target_language"]
            }
        )
    ]
    return tools

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls"""
    
    if name == "fetch":
        url = arguments.get("url")
        if not url:
            return [TextContent(type="text", text="Error: URL is required")]
            
        try:
            # Validate URL
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return [TextContent(type="text", text="Error: Invalid URL format")]
                
            # Use Jina Reader API
            reader_url = f"https://r.jina.ai/{url}"
            headers = {
                "Authorization": f"Bearer {JINA_API_KEY}",
                "User-Agent": "AI-Tools-MCP-Server/1.0"
            }
            
            response = requests.get(reader_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            content = response.text
            if not content.strip():
                return [TextContent(type="text", text="Warning: No content extracted from the URL")]
                
            return [TextContent(type="text", text=content)]
            
        except requests.exceptions.RequestException as e:
            return [TextContent(type="text", text=f"Error fetching content: {str(e)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]
    
    elif name == "search":
        query = arguments.get("query")
        if not query:
            return [TextContent(type="text", text="Error: Query is required")]
            
        try:
            # Use Jina Search API
            search_url = f"https://s.jina.ai/{query}"
            headers = {
                "Authorization": f"Bearer {JINA_API_KEY}",
                "User-Agent": "AI-Tools-MCP-Server/1.0"
            }
            
            response = requests.get(search_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            content = response.text
            if not content.strip():
                return [TextContent(type="text", text="No search results found")]
                
            return [TextContent(type="text", text=content)]
            
        except requests.exceptions.RequestException as e:
            return [TextContent(type="text", text=f"Error performing search: {str(e)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]
    
    elif name == "translate":
        if not GEMINI_API_KEY:
            return [TextContent(type="text", text="Error: GEMINI_API_KEY not configured")]
            
        text = arguments.get("text")
        target_language = arguments.get("target_language")
        source_language = arguments.get("source_language", "auto")
        
        if not text or not target_language:
            return [TextContent(type="text", text="Error: text and target_language are required")]
            
        try:
            # Simple Gemini API call for translation
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
            
            prompt = f"Translate the following text from {source_language} to {target_language}. Only return the translation, no explanations:\n\n{text}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if "candidates" in result and result["candidates"]:
                translation = result["candidates"][0]["content"]["parts"][0]["text"].strip()
                return [TextContent(type="text", text=translation)]
            else:
                return [TextContent(type="text", text="Error: No translation received")]
                
        except requests.exceptions.RequestException as e:
            return [TextContent(type="text", text=f"Error calling Gemini API: {str(e)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]
    
    elif name == "translate_deepl":
        if not DEEPL_API_KEY:
            return [TextContent(type="text", text="Error: DEEPL_API_KEY not configured")]
            
        text = arguments.get("text")
        target_language = arguments.get("target_language")
        source_language = arguments.get("source_language")
        
        if not text or not target_language:
            return [TextContent(type="text", text="Error: text and target_language are required")]
            
        try:
            url = "https://api-free.deepl.com/v2/translate"
            
            data = {
                "auth_key": DEEPL_API_KEY,
                "text": text,
                "target_lang": target_language.upper()
            }
            
            if source_language:
                data["source_lang"] = source_language.upper()
                
            response = requests.post(url, data=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if "translations" in result and result["translations"]:
                translation = result["translations"][0]["text"]
                return [TextContent(type="text", text=translation)]
            else:
                return [TextContent(type="text", text="Error: No translation received")]
                
        except requests.exceptions.RequestException as e:
            return [TextContent(type="text", text=f"Error calling DeepL API: {str(e)}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Unexpected error: {str(e)}")]
    
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

@server.list_prompts()
async def handle_list_prompts() -> List[Prompt]:
    """List available prompts"""
    return [
        Prompt(
            name="optimize_prompt",
            description="Optimize and improve user prompts for better AI interactions",
            arguments=[
                PromptArgument(
                    name="original_prompt",
                    description="The original prompt to optimize",
                    required=True
                )
            ]
        )
    ]

@server.get_prompt()
async def handle_get_prompt(name: str, arguments: Dict[str, str]) -> PromptMessage:
    """Get a specific prompt"""
    if name == "optimize_prompt":
        original_prompt = arguments.get("original_prompt", "")
        
        optimized_content = f"""
I'll help you optimize this prompt for better AI interactions:

Original prompt: {original_prompt}

Optimized version:
1. Be specific and clear about what you want
2. Include relevant context and constraints  
3. Specify the desired format for the response
4. Use examples when helpful
5. Break complex requests into steps

Here's your improved prompt:

{original_prompt} 

Please provide a detailed response with specific examples and clear explanations.
"""
        
        return PromptMessage(
            role="user",
            content=TextContent(type="text", text=optimized_content)
        )
    else:
        raise ValueError(f"Unknown prompt: {name}")

async def main():
    """Main entry point"""
    logger.info("Starting AI Tools MCP Server...")
    logger.info("Available tools: fetch, search, translate, translate_deepl")
    logger.info("Available prompts: optimize_prompt")
    logger.info(f"JINA_API_KEY configured: {'Yes' if JINA_API_KEY else 'No'}")
    logger.info(f"GEMINI_API_KEY configured: {'Yes' if GEMINI_API_KEY else 'No'}")
    logger.info(f"DEEPL_API_KEY configured: {'Yes' if DEEPL_API_KEY else 'No'}")
    
    # Run the server
    async with stdio_server() as streams:
        await server.run(*streams, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())