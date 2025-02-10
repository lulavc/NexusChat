"""Chat history manager."""
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class HistoryManager:
    """Manages chat history."""
    
    def __init__(self, history_file: Optional[str] = None):
        """Initialize history manager.
        
        Args:
            history_file: Optional path to history file
        """
        self.history: List[Dict[str, Any]] = []
        self.history_file = history_file
        logger.info("History manager initialized")
        
    def add_message(self, message: Dict[str, Any]) -> None:
        """Add message to history.
        
        Args:
            message: Message to add
        """
        try:
            self.history.append(message)
            logger.info("Message added to history")
            
            if self.history_file:
                self._save_history()
                
        except Exception as e:
            logger.error(f"Error adding message to history: {str(e)}")
            raise
            
    def get_chat_history(self) -> List[Dict[str, Any]]:
        """Get chat history.
        
        Returns:
            List of messages
        """
        try:
            if self.history_file:
                self._load_history()
                
            logger.info(f"Found {len(self.history)} messages")
            return self.history
            
        except Exception as e:
            logger.error(f"Error getting chat history: {str(e)}")
            raise
            
    def clear_history(self) -> None:
        """Clear chat history."""
        try:
            self.history = []
            logger.info("Chat history cleared")
            
            if self.history_file:
                self._save_history()
                
        except Exception as e:
            logger.error(f"Error clearing chat history: {str(e)}")
            raise
            
    def _save_history(self) -> None:
        """Save chat history to file."""
        try:
            history_path = Path(self.history_file)
            history_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(history_path, "w") as f:
                json.dump(self.history, f)
                
            logger.info(f"Chat history saved to {self.history_file}")
            
        except Exception as e:
            logger.error(f"Error saving chat history: {str(e)}")
            raise
            
    def _load_history(self) -> None:
        """Load chat history from file."""
        try:
            history_path = Path(self.history_file)
            
            if history_path.exists():
                with open(history_path) as f:
                    self.history = json.load(f)
                    
                logger.info(f"Chat history loaded from {self.history_file}")
            else:
                self.history = []
                logger.info("No chat history file found")
                
        except Exception as e:
            logger.error(f"Error loading chat history: {str(e)}")
            raise
