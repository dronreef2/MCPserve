"""Sistema de logging estruturado."""

import sys
from typing import Any
import structlog
from enhanced_mcp_server.config import settings


_LOGGING_CONFIGURED = False


def setup_logging() -> None:
    """Configura o sistema de logging estruturado."""
    global _LOGGING_CONFIGURED

    if _LOGGING_CONFIGURED:
        return

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
            structlog.dev.ConsoleRenderer(colors=True, stream=sys.stderr)
        )

    structlog.configure(
        processors=shared_processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    import logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stderr,
        level=getattr(logging, settings.log_level.upper()),
    )

    _LOGGING_CONFIGURED = True


def get_logger(name: str) -> Any:
    """Retorna um logger configurado."""
    if not _LOGGING_CONFIGURED:
        setup_logging()
    return structlog.get_logger(name)