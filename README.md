# Ollama Chat

A modern and feature-rich chat interface for Ollama models, with both desktop and web interfaces.

[![GitHub license](https://img.shields.io/github/license/lulavc/ollama-chat)](https://github.com/lulavc/ollama-chat/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/lulavc/ollama-chat)](https://github.com/lulavc/ollama-chat/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/lulavc/ollama-chat)](https://github.com/lulavc/ollama-chat/issues)
[![GitHub release](https://img.shields.io/github/release/lulavc/ollama-chat)](https://github.com/lulavc/ollama-chat/releases)

## Version
- Version: 0.91b
- Codename: ValoisBR
- Developer: lulavc
- Status: Active Development

## Overview
Ollama Chat provides a sophisticated interface for interacting with Ollama's AI models. It features both a desktop application built with Python and a web interface using modern web technologies.

## Features
### Core Features
- Modern GUI chat interface with enhanced message display
- Real-time model selection and loading
- Streaming response with syntax highlighting
- Code block formatting and language detection
- Asynchronous message handling and UI updates
- Local conversation history with SQLite
- System prompt management
- Clean and modern dark theme interface
- Support for all Ollama models
- Robust error handling and recovery
- Customizable UI themes and settings

### Desktop Application
- Native desktop experience
- System tray integration
- Keyboard shortcuts
- Local file handling

### Web Interface
- Modern responsive design
- Cross-platform compatibility
- Real-time updates
- Progressive Web App support

## Requirements

### Desktop Application
- Python 3.8+
- Ollama running locally (http://localhost:11434)
- Dependencies:
  - customtkinter>=5.2.1
  - aiohttp>=3.9.1
  - aiosqlite>=0.19.0
  - requests>=2.32.3
  - pygments>=2.17.2
  - pyyaml>=6.0.1

### Web Interface
- Node.js 18+
- npm or yarn
- Modern web browser

## Installation

### Desktop Application
1. Make sure you have Ollama installed and running
2. Clone the repository
```bash
git clone https://github.com/lulavc/ollama-chat.git
cd ollama-chat
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

### Docker Installation
1. Build and run using Docker Compose
```bash
docker-compose up -d
```

### Web Interface
1. Install Node.js dependencies
```bash
cd web
npm install
```

## Usage

### Desktop Application
Run the application:
```bash
python -m ollama_chat
```

### Web Interface
Start the development server:
```bash
cd web
npm run dev
```

### Docker
Access the application:
- Desktop GUI: http://localhost:3000
- Ollama API: http://localhost:11434

## Development

### Project Structure
See [PROJECT_TREE.md](PROJECT_TREE.md) for a detailed overview of the codebase organization.

### Architecture
- Desktop: Python with customtkinter
- Backend: Async Python with aiohttp
- Database: SQLite for persistence
- Web: TypeScript, Vite, Tailwind CSS
- Container: Docker with GPU support

### Development Setup
1. Set up development environment
```bash
./scripts/setup_dev.sh
```

2. Install development dependencies
```bash
pip install -r requirements-dev.txt
```

3. Run tests
```bash
pytest
```

## Contributing
We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Process
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

### Code Style
- Python: Follow PEP 8
- TypeScript: Use prettier
- Use type hints
- Write tests for new features

## Documentation
- [Project Tree](PROJECT_TREE.md)
- [API Documentation](docs/API.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Changelog](CHANGELOG.md)

## Support
- [Issue Tracker](https://github.com/lulavc/ollama-chat/issues)
- [Discussions](https://github.com/lulavc/ollama-chat/discussions)

## License
MIT License - See [LICENSE](LICENSE) file for details

## Acknowledgments
- Ollama Team for the amazing AI model server
- Contributors and community members
