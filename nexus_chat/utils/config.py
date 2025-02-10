"""Configuration module."""
import json
import logging
import logging.config
import os
from pathlib import Path
from typing import Dict, Optional

# Configure logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": "nexus_chat.log",
            "mode": "a"
        }
    },
    "loggers": {
        "nexus_chat": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False
        },
        "nexus_chat.backend.ollama_client": {
            "level": "DEBUG",
            "handlers": ["console", "file"],
            "propagate": False
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}

# Configure paths
PATHS = {
    "BASE_DIR": os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "HISTORY_DIR": os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "history"),
}

# Create directories if they don't exist
for path in PATHS.values():
    if not os.path.exists(path):
        os.makedirs(path)

def configure_logging():
    """Configure logging."""
    try:
        # Configure logging
        logging.config.dictConfig(LOGGING_CONFIG)
        
        # Log configuration
        logger = logging.getLogger(__name__)
        logger.info("Logging configured")
        
    except Exception as e:
        print(f"Error configuring logging: {str(e)}")
        raise

def get_config_path() -> Path:
    """Get config file path."""
    try:
        logger = logging.getLogger(__name__)
        logger.info("Getting config path")
        
        # Get config directory
        config_dir = Path.home() / ".config" / "ollama-chat"
        
        # Create directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)
        
        # Get config file path
        config_path = config_dir / "config.json"
        
        logger.info(f"Config path: {config_path}")
        return config_path
        
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error getting config path: {e}")
        raise

def load_config(config_file: Optional[Path] = None) -> Dict:
    """Load configuration from file."""
    try:
        logger = logging.getLogger(__name__)
        logger.info("Loading config")
        
        # Get config path
        config_path = config_file or get_config_path()
        logger.info(f"Loading config from {config_path}")
        
        # Create default config if file doesn't exist
        if not config_path.exists():
            logger.info("Config file not found, creating default")
            save_config({}, config_path)
        
        # Load config
        with open(config_path, "r") as f:
            config = json.load(f)
        
        logger.info("Config loaded successfully")
        return config
        
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error loading config: {e}")
        raise

def save_config(config: Dict, config_file: Optional[Path] = None) -> None:
    """Save configuration to file."""
    try:
        logger = logging.getLogger(__name__)
        logger.info("Saving config")
        
        # Get config path
        config_path = config_file or get_config_path()
        logger.info(f"Saving config to {config_path}")
        
        # Save config
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
        
        logger.info("Config saved successfully")
        
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error saving config: {e}")
        raise

configure_logging()
