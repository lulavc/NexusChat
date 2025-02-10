"""Message model."""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Optional, Dict, Any

class MessageRole(Enum):
    """Message role enum."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    
    def __str__(self):
        return self.value

@dataclass
class Message:
    """Message model."""
    
    role: MessageRole
    content: str
    model: Optional[str] = None
    created_at: datetime = None
    id: Optional[str] = None
    
    def __post_init__(self):
        """Initialize message."""
        if self.created_at is None:
            self.created_at = datetime.now()
            
        # Convert string role to enum if needed
        if isinstance(self.role, str):
            self.role = MessageRole(self.role)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message":
        """Create message from dictionary."""
        return cls(
            id=data.get("id"),
            role=MessageRole(data["role"]),
            content=data["content"],
            model=data.get("model"),
            created_at=datetime.fromisoformat(data["created_at"])
            if "created_at" in data
            else None
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary."""
        return {
            "id": self.id,
            "role": str(self.role),
            "content": self.content,
            "model": self.model,
            "created_at": self.created_at.isoformat()
        }
