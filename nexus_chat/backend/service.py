"""Backend service module."""
import asyncio
import logging
from typing import Callable, List, Optional

from nexus_chat.backend.chat_manager import ChatManager
from nexus_chat.backend.history_manager import HistoryManager
from nexus_chat.backend.ollama_client import OllamaClient
from nexus_chat.utils.config import load_config, save_config

logger = logging.getLogger(__name__)

class BackendService:
    """Backend service class."""
    
    def __init__(self):
        """Initialize backend service."""
        try:
            logger.info("Initializing backend service")
            
            # Load config
            self.config = load_config()
            
            # Create clients
            self.ollama_client = OllamaClient()
            
            # Create managers
            self.history_manager = HistoryManager()
            self.chat_manager = ChatManager(
                ollama_client=self.ollama_client,
                history_manager=self.history_manager
            )
            
            logger.info("Backend service initialized")
            
        except Exception as e:
            logger.error(f"Error initializing backend service: {str(e)}")
            raise
            
    async def start(self):
        """Start backend service."""
        try:
            logger.info("Starting backend service")
            
            # Nothing to start yet
            
            logger.info("Backend service started")
            
        except Exception as e:
            logger.error(f"Error starting backend service: {str(e)}")
            raise
            
    async def stop(self):
        """Stop backend service."""
        try:
            logger.info("Stopping backend service")
            
            # Close clients
            await self.ollama_client.close()
            
            logger.info("Backend service stopped")
            
        except Exception as e:
            logger.error(f"Error stopping backend service: {str(e)}")
            raise
            
    def set_model(self, model: str):
        """Set current model.
        
        Args:
            model: Model name
        """
        try:
            logger.info(f"Setting model to {model}")
            self.chat_manager.set_model(model)
            
            # Save to config
            self.config["model"] = model
            save_config(self.config)
            
        except Exception as e:
            logger.error(f"Error setting model: {str(e)}")
            raise
            
    def get_model(self) -> Optional[str]:
        """Get current model.
        
        Returns:
            Current model name or None
        """
        try:
            logger.info("Getting current model")
            return self.config.get("model")
            
        except Exception as e:
            logger.error(f"Error getting model: {str(e)}")
            raise
            
    async def list_models(self) -> List[str]:
        """List available models.
        
        Returns:
            List of model names
        """
        try:
            logger.info("Listing models")
            return await self.chat_manager.list_models()
            
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            raise
            
    async def send_message(self, message: str, callback: Optional[Callable[[str], None]] = None) -> str:
        """Send message to model.
        
        Args:
            message: Message text
            callback: Optional callback for streaming responses
            
        Returns:
            Model response
        """
        try:
            logger.info("Sending message")
            return await self.chat_manager.send_message(message, callback)
            
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            raise
