#!/usr/bin/env python3
"""Main module."""
import logging

from nexus_chat.gui.app import App
from nexus_chat.utils.logging_config import setup_logging

def main():
    """Run main application."""
    try:
        # Setup logging
        setup_logging()
        
        # Create application
        app = App()
        
        # Run application
        app.run()
        
    except Exception as e:
        logging.error(f"Error running application: {str(e)}")
        raise
        
if __name__ == "__main__":
    main()
