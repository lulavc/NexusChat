# src/models/base.py
from datetime import datetime
from typing import Optional, Dict, Any
import uuid
import json
from dataclasses import dataclass, asdict, field

@dataclass
class BaseModel:
    """Base class for all models in the application"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        data = asdict(self)
        # Convert datetime objects to ISO format
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data

    def to_json(self) -> str:
        """Convert model to JSON string"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """Create model instance from dictionary"""
        # Convert ISO datetime strings back to datetime objects
        if 'created_at' in data:
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data:
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> 'BaseModel':
        """Create model instance from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def update(self, **kwargs):
        """Update model attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

# src/models/message.py
from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum
from .base import BaseModel

class MessageRole(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class MessageStatus(Enum):
    PENDING = "pending"
    STREAMING = "streaming"
    COMPLETE = "complete"
    ERROR = "error"

@dataclass
class Message(BaseModel):
    """Model representing a chat message"""
    content: str
    role: MessageRole
    model: str
    session_id: str
    status: MessageStatus = MessageStatus.PENDING
    parent_id: Optional[str] = None
    children: List[str] = field(default_factory=list)
    tokens: Optional[int] = None
    error: Optional[str] = None

    def append_content(self, content: str):
        """Append content to message (used during streaming)"""
        self.content += content
        self.updated_at = datetime.now()

    def set_error(self, error: str):
        """Set error status and message"""
        self.status = MessageStatus.ERROR
        self.error = error
        self.updated_at = datetime.now()

    def complete(self):
        """Mark message as complete"""
        self.status = MessageStatus.COMPLETE
        self.updated_at = datetime.now()

# src/models/chat_session.py
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
from .base import BaseModel
from .message import Message, MessageRole

@dataclass
class ChatSession(BaseModel):
    """Model representing a chat session"""
    name: str
    model: str
    messages: List[Message] = field(default_factory=list)
    system_prompt: Optional[str] = None
    settings: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    last_message_at: Optional[datetime] = None

    def add_message(self, message: Message) -> None:
        """Add a message to the session"""
        self.messages.append(message)
        self.last_message_at = datetime.now()
        self.updated_at = datetime.now()

    def get_context_window(self, max_messages: Optional[int] = None) -> List[Message]:
        """Get messages for context window"""
        if max_messages:
            return self.messages[-max_messages:]
        return self.messages

    def get_system_message(self) -> Optional[Message]:
        """Get system prompt as a message"""
        if self.system_prompt:
            return Message(
                content=self.system_prompt,
                role=MessageRole.SYSTEM,
                model=self.model,
                session_id=self.id
            )
        return None

    def clear_messages(self) -> None:
        """Clear all messages from session"""
        self.messages.clear()
        self.updated_at = datetime.now()

# Example test file: tests/unit/test_models.py
import pytest
from datetime import datetime
from src.models.base import BaseModel
from src.models.message import Message, MessageRole
from src.models.chat_session import ChatSession

def test_base_model_creation():
    model = BaseModel()
    assert model.id is not None
    assert isinstance(model.created_at, datetime)
    assert isinstance(model.updated_at, datetime)

def test_message_creation():
    message = Message(
        content="Hello",
        role=MessageRole.USER,
        model="test-model",
        session_id="test-session"
    )
    assert message.content == "Hello"
    assert message.role == MessageRole.USER
    assert message.status == MessageStatus.PENDING

def test_chat_session_messages():
    session = ChatSession(
        name="Test Session",
        model="test-model"
    )
    message = Message(
        content="Test message",
        role=MessageRole.USER,
        model=session.model,
        session_id=session.id
    )
    session.add_message(message)
    assert len(session.messages) == 1
    assert session.last_message_at is not None