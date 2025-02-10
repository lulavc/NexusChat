"""Application configuration."""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

from nexus_chat.utils.constants import API_CONSTANTS, MESSAGE_CONSTANTS

class Config:
    """Application configuration."""
    
    def __init__(self, config_file: Optional[str] = None):
        """Initialize configuration."""
        self.config_file = config_file or self._get_default_config_file()
        self.config: Dict[str, Any] = self._load_config()
    
    def _get_default_config_file(self) -> str:
        """Get default config file path."""
        config_dir = os.path.expanduser("~/.config/ollama-chat")
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "config.json")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        # Default configuration
        config = {
            "api": {
                "host": API_CONSTANTS["DEFAULT_HOST"],
                "timeout": API_CONSTANTS["REQUEST_TIMEOUT"]
            },
            "chat": {
                "system_prompt": MESSAGE_CONSTANTS["DEFAULT_SYSTEM_PROMPT"],
                "max_context_length": MESSAGE_CONSTANTS["MAX_CONTEXT_LENGTH"],
                "max_history_length": MESSAGE_CONSTANTS["MAX_HISTORY_LENGTH"]
            },
            "ui": {
                "theme": "dark",
                "font_size": 12,
                "show_timestamps": True
            }
        }
        
        # Load from file if exists
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config.update(json.load(f))
            except Exception as e:
                print(f"Error loading config: {e}")
        
        return config
    
    def save(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        try:
            path = key.split(".")
            value = self.config
            for k in path:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any):
        """Set configuration value."""
        try:
            path = key.split(".")
            target = self.config
            for k in path[:-1]:
                target = target.setdefault(k, {})
            target[path[-1]] = value
            self.save()
        except Exception as e:
            print(f"Error setting config value: {e}")
    
    def update(self, config: Dict[str, Any]):
        """Update configuration with new values."""
        self.config.update(config)
        self.save()
