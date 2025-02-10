# Ollama Chat API Documentation

## Overview
This document describes the internal APIs and interfaces used in the Ollama Chat application.

## Backend Services

### OllamaClient
The main interface for communicating with the Ollama server.

```python
class OllamaClient:
    async def list_models() -> List[Model]
    async def load_model(model_name: str) -> bool
    async def generate_response(prompt: str, params: Dict) -> AsyncGenerator
    async def get_model_info(model_name: str) -> ModelInfo
```

### ChatManager
Handles chat sessions and message processing.

```python
class ChatManager:
    async def create_session() -> ChatSession
    async def send_message(message: Message) -> AsyncGenerator
    async def get_history(session_id: str) -> List[Message]
```

### StorageManager
Manages persistent storage of chat history and settings.

```python
class StorageManager:
    async def save_message(message: Message) -> bool
    async def get_messages(session_id: str) -> List[Message]
    async def save_settings(settings: Dict) -> bool
```

## Frontend Interfaces

### Desktop GUI

#### ChatWindow
Main chat interface component.

```python
class ChatWindow:
    def send_message(message: str) -> None
    def update_display(message: Message) -> None
    def clear_chat() -> None
```

#### ModelSelector
Model selection and management interface.

```python
class ModelSelector:
    def load_model(model_name: str) -> None
    def refresh_models() -> None
    def get_current_model() -> str
```

### Web Interface

#### REST API Endpoints

```typescript
// Chat endpoints
POST /api/chat/message
GET /api/chat/history
DELETE /api/chat/clear

// Model endpoints
GET /api/models/list
POST /api/models/load
GET /api/models/info

// Settings endpoints
GET /api/settings
PUT /api/settings
```

## Data Models

### Message
```python
@dataclass
class Message:
    id: str
    content: str
    role: str  # 'user' or 'assistant'
    timestamp: datetime
    session_id: str
```

### ChatSession
```python
@dataclass
class ChatSession:
    id: str
    model: str
    created_at: datetime
    messages: List[Message]
```

### ModelInfo
```python
@dataclass
class ModelInfo:
    name: str
    size: int
    parameters: Dict
    license: str
```

## Error Handling
All API endpoints and methods follow a consistent error handling pattern:

```python
class ChatError(Exception):
    pass

class ModelError(Exception):
    pass

class StorageError(Exception):
    pass
```

## Configuration
Settings and configuration options available through the API:

```yaml
api:
  host: localhost
  port: 11434
  timeout: 30

models:
  default: llama2
  parameters:
    temperature: 0.7
    max_length: 2000

storage:
  type: sqlite
  path: ~/.ollama_chat/history.db
```

## WebSocket Events
Real-time events for chat updates:

```typescript
interface ChatEvent {
  type: 'message' | 'status' | 'error'
  payload: any
}
```

## Security
- All API endpoints require appropriate authentication
- Rate limiting is implemented
- Input validation on all endpoints
- Secure storage of sensitive data
