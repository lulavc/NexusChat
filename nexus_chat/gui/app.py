"""Main application window."""
import asyncio
import logging
import sys
from typing import Optional

import customtkinter as ctk

from nexus_chat.backend.service import BackendService
from nexus_chat.gui.chat_window import ChatWindow
from nexus_chat.gui.model_selector import ModelSelector
from nexus_chat.utils.constants import WINDOW_DEFAULTS

logger = logging.getLogger(__name__)

class App(ctk.CTk):
    """Main application window."""
    
    def __init__(self):
        """Initialize the application."""
        try:
            logger.info("Starting NexusChat")
            
            # Initialize parent
            super().__init__()
            
            # Configure window
            self._configure_window()
            
            # Initialize event loop
            if sys.platform == 'win32':
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            
            # Initialize backend
            self._init_backend()
            
            # Initialize GUI
            self._init_gui()
            
            # Start event loop
            self.after(10, self._process_async_tasks)
            
            logger.info("NexusChat initialized")
            
        except Exception as e:
            logger.error(f"Error initializing application: {str(e)}")
            self._handle_fatal_error(e)
            
    def _configure_window(self):
        """Configure the main window."""
        try:
            # Set window title
            self.title(WINDOW_DEFAULTS["TITLE"])
            
            # Set window size
            self.geometry(f"{WINDOW_DEFAULTS['DEFAULT_WIDTH']}x{WINDOW_DEFAULTS['DEFAULT_HEIGHT']}")
            self.minsize(WINDOW_DEFAULTS["MIN_WIDTH"], WINDOW_DEFAULTS["MIN_HEIGHT"])
            
            # Configure grid
            self.grid_rowconfigure(0, weight=0)  # Model selector
            self.grid_rowconfigure(1, weight=1)  # Chat window
            self.grid_columnconfigure(0, weight=1)
            
            # Configure theme
            self.configure(fg_color="#1e1f22")
            
            # Configure protocol
            self.protocol("WM_DELETE_WINDOW", self._on_closing)
            
        except Exception as e:
            logger.error(f"Error configuring window: {str(e)}")
            raise
            
    def _init_backend(self):
        """Initialize the backend components."""
        try:
            # Create backend service
            self.backend = BackendService()
            logger.info("Backend initialized")
            
        except Exception as e:
            logger.error(f"Error initializing backend: {str(e)}")
            raise
            
    def _init_gui(self):
        """Initialize the GUI components."""
        try:
            # Create model selector
            self.model_selector = ModelSelector(
                self,
                self.backend,
                on_model_loaded=self._on_model_loaded
            )
            self.model_selector.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
            
            # Create chat window
            self.chat_window = ChatWindow(
                self,
                self.backend
            )
            self.chat_window.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
            
            logger.info("GUI initialized")
            
        except Exception as e:
            logger.error(f"Error initializing GUI: {str(e)}")
            raise
            
    def _process_async_tasks(self):
        """Process async tasks."""
        try:
            # Run one iteration of the event loop
            self.loop.call_soon(self.loop.stop)
            self.loop.run_forever()
            
            # Schedule next iteration
            self.after(10, self._process_async_tasks)
            
        except Exception as e:
            logger.error(f"Error processing async tasks: {str(e)}")
            self._handle_fatal_error(e)
            
    def _on_closing(self):
        """Handle window closing."""
        try:
            # Close backend
            self.loop.run_until_complete(self.backend.stop())
            
            # Close loop
            self.loop.close()
            
            # Destroy window
            self.quit()
            
        except Exception as e:
            logger.error(f"Error handling window closing: {str(e)}")
            raise
            
    def _handle_fatal_error(self, error: Exception):
        """Handle fatal application errors."""
        try:
            logger.error(f"Error handling fatal error: {str(error)}")
            self.quit()
            
        except Exception as e:
            logger.critical(f"Error handling fatal error: {str(e)}")
            raise
            
    def _on_model_loaded(self, model: str):
        """Handle model loaded event.
        
        Args:
            model: Name of loaded model
        """
        try:
            logger.info(f"Model loaded: {model}")
            
            # Enable chat window
            self.chat_window.enable()
            
        except Exception as e:
            logger.error(f"Error handling model loaded: {str(e)}")
            raise
            
    def run(self):
        """Run application."""
        try:
            # Start backend
            self.loop.run_until_complete(self.backend.start())
            
            # Run mainloop
            self.mainloop()
            
        except Exception as e:
            logger.error(f"Error running application: {str(e)}")
            raise
            
if __name__ == "__main__":
    app = App()
    app.run()
