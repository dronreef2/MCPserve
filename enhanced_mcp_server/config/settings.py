"""Configuração centralizada do Enhanced MCP Server."""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação."""

    # API Keys
    deepl_api_key: Optional[str] = Field(default=None, alias="DEEPL_API_KEY")
    gemini_api_key: Optional[str] = Field(default=None, alias="GEMINI_API_KEY")

    # Cache
    redis_url: Optional[str] = Field(default=None, alias="REDIS_URL")
    cache_ttl: int = Field(default=3600, alias="CACHE_TTL")  # 1 hora

    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    log_format: str = Field(default="json", alias="LOG_FORMAT")

    # Web Interface
    web_host: str = Field(default="0.0.0.0", alias="WEB_HOST")
    web_port: int = Field(default=8001, alias="WEB_PORT")
    web_reload: bool = Field(default=False, alias="WEB_RELOAD")

    # Security
    enable_auth: bool = Field(default=True, alias="ENABLE_AUTH")
    api_key_header: str = Field(default="X-API-Key", alias="API_KEY_HEADER")

    # Timeouts
    request_timeout: int = Field(default=30, alias="REQUEST_TIMEOUT")
    translation_timeout: int = Field(default=60, alias="TRANSLATION_TIMEOUT")

    # Rate Limiting
    rate_limit_requests: int = Field(default=100, alias="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, alias="RATE_LIMIT_WINDOW")  # segundos

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        populate_by_name=True,
    )


# Instância global das configurações
settings = Settings()