"""Chat session data model."""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from .message import Message

@dataclass
class ChatSession:
    """Represents a chat session with message history."""
    session_id: str
    model: str
    messages: List[Message]
    system_prompt: Optional[str]
    created_at: datetime
    updated_at: datetime
    metadata: dict = None
