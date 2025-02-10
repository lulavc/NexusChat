# Ollama Chat Project Tree

## Project Structure Overview

```
ollama_chat/                      # Main project directory
├── ollama_chat/                  # Main Python package
│   ├── __main__.py              # Entry point (936B)
│   ├── main.py                  # Main application logic (525B)
│   ├── config.py                # Configuration handling (2.97KB)
│   │
│   ├── api/                     # API related code
│   │   └── __init__.py
│   │
│   ├── backend/                 # Backend services
│   │   ├── __init__.py
│   │   ├── chat_manager.py      # Chat session management (3.55KB)
│   │   ├── history_manager.py   # Chat history handling (3.12KB)
│   │   ├── message_queue.py     # Message queue system (1.24KB)
│   │   ├── ollama_client.py     # Ollama API client (11.1KB)
│   │   ├── service.py           # Backend service coordination (3.9KB)
│   │   └── storage_manager.py   # Data persistence (8.21KB)
│   │
│   ├── gui/                     # GUI components
│   │   ├── __init__.py
│   │   ├── accessible_mixin.py  # Accessibility features (773B)
│   │   ├── api_config.py        # API configuration UI (3.08KB)
│   │   ├── app.py              # Main application window (5.75KB)
│   │   ├── async_app.py        # Async app handling (2.7KB)
│   │   ├── chat_bubble.py      # Chat message bubbles (3.35KB)
│   │   ├── chat_window.py      # Main chat interface (15.6KB)
│   │   ├── history_view.py     # Chat history viewer (5.32KB)
│   │   ├── model_selector.py   # Model selection UI (8.43KB)
│   │   ├── model_settings.py   # Model configuration (2.29KB)
│   │   ├── preferences.py      # User preferences UI (1.69KB)
│   │   ├── settings_panel.py   # Settings interface (4.31KB)
│   │   ├── styles.py          # UI styling (4.79KB)
│   │   └── theme.py           # Theme management (764B)
│   │
│   ├── models/                 # Data models
│   │   ├── __init__.py        # Package init (126B)
│   │   ├── chat_session.py    # Session model (1.4KB)
│   │   ├── message.py         # Message model (1.55KB)
│   │   ├── session.py         # Session handling (419B)
│   │   └── settings.py        # Settings model (9.79KB)
│   │
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── async_helper.py     # Async utilities (3.39KB)
│       ├── config.py          # Config management (4.34KB)
│       ├── constants.py       # App constants (3.87KB)
│       ├── exceptions.py      # Custom exceptions (577B)
│       ├── logger.py         # Logging system (2.63KB)
│       ├── logging_config.py # Log configuration (1.24KB)
│       ├── stream_handler.py # Stream processing (1.7KB)
│       ├── theme_manager.py  # Theme handling (742B)
│       └── validators.py     # Input validation (694B)
│
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── conftest.py           # Test configuration
│   ├── test_chat.py         # Chat tests
│   ├── test_models.py       # Model tests
│   └── test_utils.py        # Utility tests
│
├── scripts/                   # Utility scripts
│   └── setup_dev.sh         # Development setup
│
├── docs/                     # Documentation
│   ├── 0.0-IMPORTANTE.md    # Important notes (336B)
│   ├── 0.1-GraphTD.md       # Technical design (503B)
│   ├── 0.2project-structure.md # Structure docs (1.38KB)
│   ├── 0.3-project-base.md    # Base implementation (2.13KB)
│   ├── 0.4-data-models.md     # Data model docs (4.74KB)
│   ├── 0.5-backend-services.md # Backend docs (4.79KB)
│   ├── 0.6-enhanced-ollama-chat.md # Enhanced features (9.94KB)
│   ├── 1-implementation-guide.md    # Implementation guide (4.9KB)
│   └── 2-base-models.md            # Model documentation (5.66KB)
│
├── web/                      # Web interface
│   ├── src/                 # Source files
│   ├── public/             # Public assets
│   ├── package.json        # Node.js dependencies (1KB)
│   ├── tsconfig.json      # TypeScript config (641B)
│   └── vite.config.ts     # Vite configuration (206B)
│
├── docker/                  # Docker configuration
│   ├── Dockerfile         # Container config (336B)
│   └── docker-compose.yml # Container orchestration (694B)
│
├── .git/                   # Git repository
├── .gitignore             # Git ignore rules (13B)
├── CHANGELOG.md           # Version history (1.22KB)
├── LICENSE               # MIT License
├── README.md             # Project overview (1.86KB)
├── requirements.txt      # Python dependencies (102B)
├── setup.py             # Package setup (347B)
└── pytest.ini           # Test configuration (77B)

## Key Directories

### /ollama_chat
Main Python package containing all core functionality. Organized into:
- Backend services for API communication and data management
- GUI components for user interface
- Data models for business logic
- Utility functions and helpers

### /tests
Test suite with pytest configuration and test cases for:
- Chat functionality
- Model operations
- Utility functions
- Integration tests

### /docs
Comprehensive documentation covering:
- Technical design
- Implementation guides
- Data models
- Backend services
- Enhanced features

### /web
Web interface implementation using:
- TypeScript
- Vite
- Modern web technologies
- Tailwind CSS

### /docker
Container configuration for:
- Development environment
- Production deployment
- GPU support
- Service orchestration

## File Sizes and Statistics
- Largest source file: chat_window.py (15.6KB)
- Largest documentation: enhanced-ollama-chat.md (9.94KB)
- Total Python files: ~50
- Total documentation files: ~15
- Configuration files: ~10

## Development Status
- Version: 0.91b
- Active development
- Regular updates
- Comprehensive testing
- Docker support
- Multiple deployment options
```
