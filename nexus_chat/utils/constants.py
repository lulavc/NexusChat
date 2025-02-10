"""Global constants and configurations."""
from enum import Enum
from typing import Dict

# API Endpoints
API_ENDPOINTS = {
    "generate": "/api/generate",
    "models": "/api/tags",
    "chat": "/api/chat"
}

# Message Roles
class MessageRole(Enum):
    """Available message roles."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

# Default System Prompts
DEFAULT_SYSTEM_PROMPTS: Dict[str, str] = {
    "default": """You are a helpful AI assistant.""",
    
    "code": """You are a helpful programming assistant. You help users write, 
    debug, and understand code. You provide clear explanations and follow best 
    practices.""",
    
    "creative": """You are a creative writing assistant. You help users with 
    writing tasks, providing suggestions and feedback while maintaining their 
    unique voice.""",
    
    "academic": """You are a knowledgeable academic assistant. You help users 
    with research, writing, and understanding complex topics while maintaining 
    academic rigor."""
}

# UI Constants
WINDOW_DEFAULTS = {
    "TITLE": "NexusChat",
    "DEFAULT_WIDTH": 800,
    "DEFAULT_HEIGHT": 600,
    "MIN_WIDTH": 400,
    "MIN_HEIGHT": 300,
}

GUI_CONSTANTS = {
    # Padding
    "SMALL_PADDING": 5,
    "MEDIUM_PADDING": 10,
    "LARGE_PADDING": 20,
    
    # Colors
    "PRIMARY_COLOR": "#2B2D42",
    "SECONDARY_COLOR": "#8D99AE",
    "ACCENT_COLOR": "#EF233C",
    "BACKGROUND_COLOR": "#EDF2F4",
    "TEXT_COLOR": "#2B2D42",
    "ERROR_COLOR": "#D90429",
    "SUCCESS_COLOR": "#4CAF50",
    "WARNING_COLOR": "#FFC107",
    "INFO_COLOR": "#2196F3",
    "HOVER_COLOR": "#7D8A9E",
    "ACCENT_COLOR_HOVER": "#DF132C",
    "BORDER_COLOR": "#8D99AE",
    "PLACEHOLDER_COLOR": "#8D99AE",
    
    # Fonts
    "DEFAULT_FONT": ("Arial", 12),
    "SMALL_FONT": ("Arial", 10),
    "LARGE_FONT": ("Arial", 14),
    
    # Style
    "BORDER_RADIUS": 10,
    "BORDER_WIDTH": 1,
    
    # Input height
    "INPUT_HEIGHT": 100,
    
    # Chat bubble
    "BUBBLE_MAX_HEIGHT": 200,
    "BUBBLE_MIN_HEIGHT": 50,
    "BUBBLE_LINE_HEIGHT": 20
}

CHAT_WINDOW_DEFAULTS = {
    "FONT_SIZE": 12,
    "INPUT_HEIGHT": 100,
}

MODEL_SELECTOR_DEFAULTS = {
    "FONT_SIZE": 12,
    "COMBOBOX_WIDTH": 200,
    "BUTTON_WIDTH": 100,
}

API_CONSTANTS = {
    # API settings
    "OLLAMA_API_URL": "http://localhost:11434",
    "REQUEST_TIMEOUT": 60,  # seconds
}

MESSAGE_CONSTANTS = {
    # Message settings
    "DEFAULT_SYSTEM_PROMPT": """You are a helpful AI assistant.""",
    "MAX_CONTEXT_LENGTH": 4096,
    "MAX_HISTORY_LENGTH": 100,
}

CHAT_WINDOW = {
    "MAX_MESSAGE_LENGTH": 4000,
}

MODEL_DEFAULTS = {
    "DEFAULT_MODEL": "llama2",
    "CONTEXT_LENGTH": 4096,
    "MAX_TOKENS": 2048,
    "TEMPERATURE": 0.7,
    "TOP_P": 0.9,
    "TOP_K": 40,
    "REPETITION_PENALTY": 1.1
}

# Error Messages
ERROR_MESSAGES = {
    "API_ERROR": "Error communicating with Ollama API: {error}",
    "MODEL_ERROR": "Error loading model {model}: {error}",
    "STORAGE_ERROR": "Error accessing storage: {error}",
    "SESSION_ERROR": "Error with chat session: {error}",
    "CONFIG_ERROR": "Error loading configuration: {error}"
}

# Success Messages
SUCCESS_MESSAGES = {
    "MODEL_LOADED": "Model {model} loaded successfully",
    "SESSION_CREATED": "New chat session created",
    "SETTINGS_SAVED": "Settings saved successfully",
    "BACKUP_CREATED": "Backup created successfully"
}

# File Extensions
FILE_EXTENSIONS = {
    "SETTINGS": ".json",
    "DATABASE": ".db",
    "BACKUP": ".bak",
    "LOG": ".log"
}

# Logging Constants
LOGGING = {
    "DEFAULT_LEVEL": "INFO",
    "MAX_FILE_SIZE": 10 * 1024 * 1024,  # 10MB
    "BACKUP_COUNT": 5,
    "DATE_FORMAT": "%Y-%m-%d %H:%M:%S"
}

# Storage Constants
DATABASE = {
    "MAX_HISTORY": 100,
    "BACKUP_INTERVAL": 24,  # hours
    "MAX_BACKUP_AGE": 30,   # days
    "MAX_BACKUP_SIZE": 100  # MB
}
