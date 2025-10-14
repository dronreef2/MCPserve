"""Configuração centralizada do Enhanced MCP Server."""

import os
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação."""

    # API Keys
    jina_api_key: Optional[str] = Field(default=None, env="JINA_API_KEY")
    gemini_api_key: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    deepl_api_key: Optional[str] = Field(default=None, env="DEEPL_API_KEY")

    # Cache
    redis_url: Optional[str] = Field(default=None, env="REDIS_URL")
    cache_ttl: int = Field(default=3600, env="CACHE_TTL")  # 1 hora

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")

    # Web Interface
    web_host: str = Field(default="0.0.0.0", env="WEB_HOST")
    web_port: int = Field(default=8001, env="WEB_PORT")
    web_reload: bool = Field(default=False, env="WEB_RELOAD")

    # Security
    enable_auth: bool = Field(default=True, env="ENABLE_AUTH")
    api_key_header: str = Field(default="X-API-Key", env="API_KEY_HEADER")

    # Timeouts
    request_timeout: int = Field(default=30, env="REQUEST_TIMEOUT")
    translation_timeout: int = Field(default=60, env="TRANSLATION_TIMEOUT")

    # Rate Limiting
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, env="RATE_LIMIT_WINDOW")  # segundos

    class Config:
        env_file = ".env"
        case_sensitive = False


# Instância global das configurações
settings = Settings()