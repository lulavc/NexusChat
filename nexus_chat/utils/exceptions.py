"""Exception classes for the application."""

class ChatError(Exception):
    """Base class for chat-related exceptions."""
    pass

class NoActiveSessionError(ChatError):
    """Raised when trying to perform operations without an active session."""
    pass

class SessionInitializationError(ChatError):
    """Raised when session initialization fails."""
    pass

class ModelNotFoundError(ChatError):
    """Raised when the requested model is not found."""
    pass

class OllamaConnectionError(ChatError):
    """Raised when connection to Ollama server fails."""
    pass
