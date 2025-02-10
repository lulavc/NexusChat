"""Logging configuration and utilities."""
import logging
import sys
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler

def setup_logger(
    name: str = "nexus_chat",
    level: str = "INFO",
    log_file: Optional[Path] = None,
    console: bool = True,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """Configure and return a logger instance.
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Optional path to log file
        console: Whether to log to console
        max_bytes: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Create formatters
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_formatter = logging.Formatter(
        '%(levelname)s: %(message)s'
    )
    
    # Add file handler if log_file specified
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    # Add console handler if requested
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    return logger

def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """Log an error with full traceback and context."""
    if context:
        logger.error(f"Error in {context}: {str(error)}", exc_info=True)
    else:
        logger.error(str(error), exc_info=True)

def log_warning(logger: logging.Logger, message: str, context: str = ""):
    """Log a warning message with optional context."""
    if context:
        logger.warning(f"{context}: {message}")
    else:
        logger.warning(message)

def log_info(logger: logging.Logger, message: str, context: str = ""):
    """Log an info message with optional context."""
    if context:
        logger.info(f"{context}: {message}")
    else:
        logger.info(message)

def log_debug(logger: logging.Logger, message: str, context: str = ""):
    """Log a debug message with optional context."""
    if context:
        logger.debug(f"{context}: {message}")
    else:
        logger.debug(message)
