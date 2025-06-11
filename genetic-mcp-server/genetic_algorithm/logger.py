import structlog
import logging

from typing import Optional

def logger_config(process_name: Optional[str], pretty: Optional[bool] = True):
    """
    Configure the logger to use structlog with optional pretty-print output.

    :param pretty: Whether to enable pretty-printing for logs.
    """
    logging.basicConfig(level=logging.DEBUG)

    processors = [
        structlog.processors.TimeStamper(fmt="iso"),  # Add timestamp to logs
        structlog.dev.ConsoleRenderer() if pretty else structlog.processors.JSONRenderer(),
    ]

    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logger = structlog.get_logger()
    if process_name:
        logger = logger.bind(process=process_name)

    return logger