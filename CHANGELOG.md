# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.91b] - 2025-02-10

### Added
- Web interface with TypeScript and Vite
- Docker support with GPU capabilities
- Comprehensive documentation
- Development environment setup
- GitHub integration and workflows
- Code style enforcement with Black and Prettier
- Testing infrastructure with pytest
- API documentation
- Contributing guidelines

### Enhanced
- Improved project structure and organization
- Better error handling and recovery
- Enhanced async operations
- Updated dependencies
- Expanded configuration options
- Improved logging system

### Fixed
- Various bug fixes and performance improvements
- Code style consistency
- Documentation accuracy
- Test coverage

## [0.90b] - 2025-02-01

### Added
- Initial release of Ollama Chat
- Basic chat functionality
- Model selection
- Message history
- Settings management
- Dark theme support
- Code syntax highlighting

## [0.2.0] - 2025-02-10
### Added
- Enhanced text display with syntax highlighting
- Code block formatting with language detection
- Improved async handling in model selector
- Proper session management in Ollama client
- New UI theme system with dark mode
- Keyboard shortcuts for common actions
- YAML configuration support

### Changed
- Refactored async operations for better stability
- Improved error handling and recovery
- Enhanced message queue processing
- Updated dependencies to latest versions
- Modernized UI components

### Fixed
- Model loading state handling
- Session cleanup on application exit
- Message streaming synchronization
- Code block formatting issues
- UI responsiveness during long operations

## [0.1.0] - 2025-02-09
### Added
- Initial project structure with core components:
  - GUI Layer (Chat Window, Model Selector, Settings Panel)
  - Backend Service (Ollama API Client, Chat Manager)
  - Local history storage system
- Basic message queue implementation
- Stream response handling from Ollama server

### Changed
- Improved error handling for API connections
- Refactored chat history management module

### Fixed
- Thread synchronization issues in message processing
