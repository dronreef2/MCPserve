"""Sistema de logging estruturado."""

import sys
from typing import Any, Dict
import structlog
from enhanced_mcp_server.config import settings


def setup_logging() -> None:
    """Configura o sistema de logging estruturado."""
    shared_processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]

    if settings.log_format == "json":
        shared_processors.append(structlog.processors.JSONRenderer())
    else:
        shared_processors.append(
            structlog.dev.ConsoleRenderer(colors=True)
        )

    structlog.configure(
        processors=shared_processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configura o logger padrão do Python
    import logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper()),
    )


def get_logger(name: str) -> Any:
    """Retorna um logger configurado."""
    return structlog.get_logger(name)