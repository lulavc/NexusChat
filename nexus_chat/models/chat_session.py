"""Chat session model."""
import uuid
from datetime import datetime
from typing import List, Dict, Any

class ChatSession:
    """Chat session model."""
    
    def __init__(self, model: str):
        """Initialize chat session."""
        self.id = str(uuid.uuid4())
        self.model = model
        self.name = f"Chat with {model}"
        self.created_at = datetime.now().isoformat()
        self.messages: List[Dict[str, Any]] = []
    
    def add_message(self, role: str, content: str) -> Dict[str, Any]:
        """Add a message to the session."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.messages.append(message)
        return message
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary."""
        return {
            "id": self.id,
            "model": self.model,
            "name": self.name,
            "created_at": self.created_at,
            "messages": self.messages
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatSession":
        """Create session from dictionary."""
        session = cls(data["model"])
        session.id = data["id"]
        session.name = data["name"]
        session.created_at = data["created_at"]
        session.messages = data["messages"]
        return session
