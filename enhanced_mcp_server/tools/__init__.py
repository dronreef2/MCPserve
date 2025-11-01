"""Ferramentas MCP para busca e tradução."""

import re
from urllib.parse import urlparse
import httpx
from enhanced_mcp_server.config import settings
from enhanced_mcp_server.utils.logging import get_logger

logger = get_logger(__name__)


class ValidationError(Exception):
    """Erro de validação."""
    pass


def validate_url(url: str) -> bool:
    """Valida se a URL é segura e bem-formada."""
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return False

        # Aceita apenas HTTP e HTTPS
        if parsed.scheme.lower() not in ['http', 'https']:
            return False

        # Bloqueia URLs perigosas
        dangerous_patterns = [
            r'\b(?:localhost|127\.0\.0\.1|0\.0\.0\.0)\b',
            r'\b(?:10\.|172\.1[6-9]\.|172\.2[0-9]\.|172\.3[0-1]\.|192\.168\.)\b',
            r'\.local\b',
            r'\.internal\b',
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                logger.warning(f"Blocked dangerous URL: {url}")
                return False

        return True
    except Exception:
        return False


def validate_language_code(code: str) -> bool:
    """Valida código de idioma."""
    supported_languages = {
        'AR', 'BG', 'CS', 'DA', 'DE', 'EL', 'EN', 'EN-GB', 'EN-US', 'ES', 'ET', 'FI', 'FR',
        'HU', 'ID', 'IT', 'JA', 'KO', 'LT', 'LV', 'NB', 'NL', 'PL', 'PT-BR', 'PT-PT',
        'RO', 'RU', 'SK', 'SL', 'SV', 'TR', 'UK', 'ZH', 'ZH-HANS', 'ZH-HANT'
    }
    return code.upper() in supported_languages


async def translate_with_deepl(content: str, source_lang: str, target_lang: str) -> str:
    """Traduz texto usando DeepL."""
    if not settings.deepl_api_key:
        raise ValidationError("DEEPL_API_KEY não configurada")

    if not validate_language_code(source_lang):
        raise ValidationError(f"Idioma de origem inválido: {source_lang}")

    if not validate_language_code(target_lang):
        raise ValidationError(f"Idioma de destino inválido: {target_lang}")

    try:
        async with httpx.AsyncClient(timeout=settings.translation_timeout) as client:
            response = await client.post(
                "https://nav.programnotes.cn/translate",
                json={
                    "text": content,
                    "source_lang": source_lang.upper(),
                    "target_lang": target_lang.upper()
                }
            )
            response.raise_for_status()
            return response.json().get("translated_text", response.text)
    except httpx.TimeoutException:
        raise ValidationError("Timeout na tradução")
    except Exception as e:
        logger.error(f"Erro na tradução com DeepL: {e}")
        raise ValidationError(f"Erro na tradução: {str(e)}")
