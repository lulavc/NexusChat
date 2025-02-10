"""Logging configuration module."""
import logging
import sys
from pathlib import Path

def setup_logging():
    """Configure logging for the application."""
    try:
        # Create logs directory if it doesn't exist
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Configure logging format
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S,%f"
        
        # Configure root logger
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            datefmt=date_format,
            handlers=[
                # Console handler
                logging.StreamHandler(sys.stdout),
                # File handler
                logging.FileHandler(
                    filename=logs_dir / "nexus_chat.log",
                    encoding="utf-8"
                )
            ]
        )
        
        # Set third-party loggers to WARNING
        logging.getLogger("PIL").setLevel(logging.WARNING)
        logging.getLogger("matplotlib").setLevel(logging.WARNING)
        
    except Exception as e:
        print(f"Error configuring logging: {str(e)}", file=sys.stderr)
        sys.exit(1)
