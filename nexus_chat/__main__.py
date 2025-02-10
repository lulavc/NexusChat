"""Main module."""
import logging
import sys
from pathlib import Path

from nexus_chat.gui.app import App
from nexus_chat.utils.config import load_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def main():
    """Run main application."""
    try:
        # Load config
        config_dir = Path.home() / ".config" / "ollama-chat"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        config_file = config_dir / "config.json"
        if not config_file.exists():
            config_file.write_text("{}")
        
        load_config(config_file)
        
        # Create and start application
        app = App()
        app.start()
        
    except Exception as e:
        logger.error(f"Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
