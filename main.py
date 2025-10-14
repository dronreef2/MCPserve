import os
import logging
import re
from typing import Optional
import requests
from urllib.parse import urlparse
from mcp.server.fastmcp import FastMCP
from gpt import call_gemini
from prompt import get_prompt
from cache import cache

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastMCP("ai-tools")

# Configuration class with validation
class Config:
    def __init__(self):
        self.jina_api_key = self._validate_api_key("JINA_API_KEY")
        self.gemini_api_key = self._validate_api_key("GEMINI_API_KEY", required=False)
        self.deepl_api_key = self._validate_api_key("DEEPL_API_KEY", required=False)

    def _validate_api_key(self, key: str, required: bool = True) -> Optional[str]:
        value = os.getenv(key)
        if required and not value:
            logger.error(f"Required environment variable {key} not set")
            raise ValueError(f"Required environment variable {key} not set")
        if value and not self._is_valid_api_key_format(value):
            logger.warning(f"API key {key} format may be invalid")
        return value

    def _is_valid_api_key_format(self, key: str) -> bool:
        """Basic validation for API key format"""
        # Jina keys typically start with "jina_"
        if key.startswith("jina_") and len(key) > 10:
            return True
        # Generic validation: alphanumeric, underscores, hyphens, reasonable length
        return bool(re.match(r'^[a-zA-Z0-9_-]{10,}$', key))

# Initialize configuration
try:
    config = Config()
    logger.info("Configuration loaded successfully")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise

@app.tool()
@cache.cached(ttl=1800)  # Cache for 30 minutes
async def fetch(url: str) -> str:
    """Fetch the content of a web page using Jina AI."""
    try:
        # Validate URL format
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            return "Error: Invalid URL format. Please provide a valid URL (e.g., https://example.com)"

        # Check for potentially malicious URLs
        if any(blocked in url.lower() for blocked in ['localhost', '127.0.0.1', '0.0.0.0']):
            return "Error: Access to local/private URLs is not allowed"

        logger.info(f"Fetching content from: {url}")

        # Use config instead of direct env access
        if not config.jina_api_key:
            return "Error: JINA_API_KEY not configured"

        headers = {"Authorization": f"Bearer {config.jina_api_key}"}

        # Add timeout and retry logic
        response = requests.get(
            f"https://r.jina.ai/{url}",
            headers=headers,
            timeout=30,
            allow_redirects=True
        )

        if response.status_code == 200:
            content = response.text
            logger.info(f"Successfully fetched content from {url} ({len(content)} chars)")
            return content
        elif response.status_code == 401:
            return "Error: Invalid API key"
        elif response.status_code == 429:
            return "Error: Rate limit exceeded. Please try again later"
        else:
            logger.error(f"HTTP {response.status_code} when fetching {url}")
            return f"Error fetching {url}: HTTP {response.status_code}"

    except requests.exceptions.Timeout:
        logger.error(f"Timeout when fetching {url}")
        return "Error: Request timed out. Please try again"
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error when fetching {url}")
        return "Error: Connection failed. Please check the URL and try again"
    except Exception as e:
        logger.error(f"Unexpected error fetching {url}: {str(e)}")
        return "Error: An unexpected error occurred while fetching the content"

@app.tool()
@cache.cached(ttl=600)  # Cache for 10 minutes
async def search(query: str) -> str:
    """Search the web using Jina AI."""
    try:
        # Validate query
        if not query or len(query.strip()) == 0:
            return "Error: Search query cannot be empty"

        if len(query) > 500:
            return "Error: Search query too long (max 500 characters)"

        # Check for potentially harmful queries
        blocked_terms = ['password', 'api_key', 'token', 'secret']
        if any(term in query.lower() for term in blocked_terms):
            return "Error: Query contains blocked terms"

        logger.info(f"Searching for: {query}")

        if not config.jina_api_key:
            return "Error: JINA_API_KEY not configured"

        headers = {"Authorization": f"Bearer {config.jina_api_key}"}

        response = requests.get(
            f"https://s.jina.ai/{query}",
            headers=headers,
            timeout=30
        )

        if response.status_code == 200:
            content = response.text
            logger.info(f"Successfully searched for '{query}' ({len(content)} chars)")
            return content
        elif response.status_code == 401:
            return "Error: Invalid API key"
        elif response.status_code == 429:
            return "Error: Rate limit exceeded. Please try again later"
        else:
            logger.error(f"HTTP {response.status_code} when searching '{query}'")
            return f"Error searching '{query}': HTTP {response.status_code}"

    except requests.exceptions.Timeout:
        logger.error(f"Timeout when searching '{query}'")
        return "Error: Search request timed out. Please try again"
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error when searching '{query}'")
        return "Error: Connection failed. Please try again"
    except Exception as e:
        logger.error(f"Unexpected error searching '{query}': {str(e)}")
        return "Error: An unexpected error occurred while searching"

@app.tool()
@cache.cached(ttl=3600)  # Cache for 1 hour
async def translate(text: str, from_lang: str = "zh", to_lang: str = "en") -> str:
    """Translate text between Chinese and English using Gemini."""
    try:
        # Validate input
        if not text or len(text.strip()) == 0:
            return "Error: Text to translate cannot be empty"

        if len(text) > 10000:
            return "Error: Text too long (max 10,000 characters)"

        # Validate language codes
        supported_langs = ['zh', 'en', 'zh-cn', 'zh-tw', 'en-us', 'en-gb']
        if from_lang.lower() not in supported_langs or to_lang.lower() not in supported_langs:
            return f"Error: Unsupported language. Supported: {', '.join(supported_langs)}"

        if from_lang.lower() == to_lang.lower():
            return "Error: Source and target languages must be different"

        logger.info(f"Translating text from {from_lang} to {to_lang} ({len(text)} chars)")

        if not config.gemini_api_key:
            return "Error: GEMINI_API_KEY not configured"

        prompt = f"Translate the following {from_lang} text to {to_lang}: {text}"

        try:
            result = call_gemini(prompt)
            logger.info(f"Successfully translated text from {from_lang} to {to_lang}")
            return result
        except Exception as api_error:
            logger.error(f"Gemini API error: {str(api_error)}")
            return "Error: Translation service temporarily unavailable. Please try again later"

    except Exception as e:
        logger.error(f"Unexpected error in translate: {str(e)}")
        return "Error: An unexpected error occurred during translation"

@app.tool()
@cache.cached(ttl=3600)  # Cache for 1 hour
async def translate_deepl(text: str, from_lang: str = "auto", to_lang: str = "en") -> str:
    """Translate text using DeepL API."""
    try:
        # Validate input
        if not text or len(text.strip()) == 0:
            return "Error: Text to translate cannot be empty"

        if len(text) > 5000:
            return "Error: Text too long (max 5,000 characters)"

        # DeepL supported languages
        supported_langs = [
            'AR', 'BG', 'CS', 'DA', 'DE', 'EL', 'EN-GB', 'EN-US', 'ES', 'ET', 'FI', 'FR',
            'HU', 'ID', 'IT', 'JA', 'KO', 'LT', 'LV', 'NB', 'NL', 'PL', 'PT-BR', 'PT-PT',
            'RO', 'RU', 'SK', 'SL', 'SV', 'TR', 'UK', 'ZH', 'ZH-HANS', 'ZH-HANT', 'AUTO'
        ]

        from_lang_upper = from_lang.upper()
        to_lang_upper = to_lang.upper()

        if from_lang_upper not in supported_langs or to_lang_upper not in supported_langs:
            return f"Error: Unsupported language. Supported languages include: {', '.join(supported_langs[:10])}..."

        if from_lang_upper == to_lang_upper and from_lang_upper != 'AUTO':
            return "Error: Source and target languages must be different"

        logger.info(f"Translating with DeepL from {from_lang_upper} to {to_lang_upper} ({len(text)} chars)")

        if not config.deepl_api_key:
            return "Error: DEEPL_API_KEY not configured"

        url = "https://api-free.deepl.com/v2/translate"
        data = {
            "text": text,
            "source_lang": from_lang_upper,
            "target_lang": to_lang_upper
        }
        headers = {
            "Authorization": f"DeepL-Auth-Key {config.deepl_api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=data, headers=headers, timeout=30)

        if response.status_code == 200:
            result = response.json()
            if 'translations' in result and len(result['translations']) > 0:
                translated_text = result['translations'][0]['text']
                logger.info(f"Successfully translated with DeepL from {from_lang_upper} to {to_lang_upper}")
                return translated_text
            else:
                return "Error: Invalid response format from DeepL"
        elif response.status_code == 401:
            return "Error: Invalid DeepL API key"
        elif response.status_code == 429:
            return "Error: DeepL rate limit exceeded. Please try again later"
        elif response.status_code == 456:
            return "Error: DeepL quota exceeded. Please check your account"
        else:
            logger.error(f"DeepL API error: HTTP {response.status_code}")
            return f"Error: DeepL service error (HTTP {response.status_code})"

    except requests.exceptions.Timeout:
        logger.error("Timeout when calling DeepL API")
        return "Error: Translation request timed out. Please try again"
    except requests.exceptions.ConnectionError:
        logger.error("Connection error when calling DeepL API")
        return "Error: Connection failed. Please try again"
    except Exception as e:
        logger.error(f"Unexpected error in translate_deepl: {str(e)}")
        return "Error: An unexpected error occurred during translation"

@app.prompt()
def optimize_prompt(user_prompt: str) -> str:
    """Optimize a user prompt using detailed templates."""
    try:
        # Validate input
        if not user_prompt or len(user_prompt.strip()) == 0:
            return "Error: Prompt to optimize cannot be empty"

        if len(user_prompt) > 5000:
            return "Error: Prompt too long (max 5,000 characters)"

        logger.info(f"Optimizing prompt ({len(user_prompt)} chars)")

        # Get optimized prompt from template
        result = get_prompt(user_prompt)

        logger.info("Successfully optimized prompt")
        return result

    except Exception as e:
        logger.error(f"Error optimizing prompt: {str(e)}")
        return "Error: Failed to optimize prompt. Please try again"

if __name__ == "__main__":
    try:
        logger.info("Starting AI Tools MCP Server...")
        logger.info("Available tools: fetch, search, translate, translate_deepl")
        logger.info("Available prompts: optimize_prompt")

        # Log configuration status
        logger.info(f"JINA_API_KEY configured: {'Yes' if config.jina_api_key else 'No'}")
        logger.info(f"GEMINI_API_KEY configured: {'Yes' if config.gemini_api_key else 'No'}")
        logger.info(f"DEEPL_API_KEY configured: {'Yes' if config.deepl_api_key else 'No'}")

        app.run()

    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        raise