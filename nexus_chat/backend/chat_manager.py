"""Chat manager module."""
import logging
from typing import Any, AsyncGenerator, Callable, Dict, List, Optional

from nexus_chat.backend.history_manager import HistoryManager
from nexus_chat.backend.ollama_client import OllamaClient
from nexus_chat.models.message import Message, MessageRole

logger = logging.getLogger(__name__)

class ChatManager:
    """Chat manager class."""
    
    def __init__(
        self,
        ollama_client: OllamaClient,
        history_manager: HistoryManager
    ):
        """Initialize chat manager.
        
        Args:
            ollama_client: Ollama client
            history_manager: History manager
        """
        try:
            logger.info("Initializing chat manager")
            
            # Store references
            self.ollama_client = ollama_client
            self.history_manager = history_manager
            
            # Initialize state
            self.current_model = None
            
            logger.info("Chat manager initialized")
            
        except Exception as e:
            logger.error(f"Error initializing chat manager: {str(e)}")
            raise
            
    def set_model(self, model: str):
        """Set current model.
        
        Args:
            model: Model name
        """
        try:
            logger.info(f"Setting model to {model}")
            self.current_model = model
        except Exception as e:
            logger.error(f"Error setting model: {str(e)}")
            raise
            
    async def list_models(self) -> list:
        """List available models."""
        try:
            logger.info("Listing models")
            return await self.ollama_client.list_models()
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
            raise
            
    async def send_message(self, message: str, callback: Callable[[str], None] = None) -> str:
        """Send message to model.
        
        Args:
            message: Message text
            callback: Optional callback to receive response chunks
            
        Returns:
            Complete model response
        """
        try:
            logger.info("Sending message")
            
            # Check model
            if not self.current_model:
                raise ValueError("No model selected")
                
            # Add user message to history
            self.history_manager.add_message(
                Message(
                    role=MessageRole.USER,
                    content=message
                )
            )
            
            # Initialize complete response
            complete_response = ""
            
            # Send message and process streaming response
            async for chunk in self.ollama_client.chat(
                model=self.current_model,
                message=message
            ):
                # Update complete response
                complete_response += chunk
                
                # Call callback if provided
                if callback:
                    callback(chunk)
                    
            # Add assistant message to history
            self.history_manager.add_message(
                Message(
                    role=MessageRole.ASSISTANT,
                    content=complete_response
                )
            )
            
            return complete_response
            
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            raise
