"""Logging utilities for AI Analytics Library."""

import logging
import sys
from typing import Optional

from ai_analytics.config import Settings


def get_logger(name: str, settings: Optional[Settings] = None) -> logging.Logger:
    """Get a configured logger instance.
    
    Args:
        name: Name for the logger.
        settings: Optional settings instance for configuration.
        
    Returns:
        Configured logging.Logger instance.
    """
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        if settings:
            logger.setLevel(settings.log_level)
        else:
            logger.setLevel(logging.INFO)
    
    return logger