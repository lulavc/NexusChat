# Ollama Chat Development Guide

## Development Environment Setup

### Prerequisites
1. Python 3.8+
2. Node.js 18+
3. Docker (optional)
4. Git

### Initial Setup

1. Clone the repository
```bash
git clone https://github.com/lulavc/ollama-chat.git
cd ollama-chat
```

2. Create a Python virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. Set up pre-commit hooks
```bash
pre-commit install
```

5. Install Node.js dependencies (for web interface)
```bash
cd web
npm install
```

## Project Structure

### Core Components
- `ollama_chat/`: Main Python package
  - `api/`: API client and interfaces
  - `backend/`: Core backend services
  - `gui/`: Desktop GUI components
  - `models/`: Data models and types
  - `utils/`: Utility functions

### Web Interface
- `web/`: Web application
  - `src/`: Source code
  - `public/`: Static assets
  - `components/`: React components
  - `styles/`: CSS and styling

### Testing
- `tests/`: Test suite
  - `unit/`: Unit tests
  - `integration/`: Integration tests
  - `e2e/`: End-to-end tests

## Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 2. Development Process
1. Write tests first (TDD approach)
2. Implement the feature
3. Run tests locally
4. Format and lint code
5. Update documentation

### 3. Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_file.py

# Run with coverage
pytest --cov=ollama_chat tests/
```

### 4. Code Style
- Use Black for Python formatting
```bash
black ollama_chat tests
```

- Sort imports with isort
```bash
isort ollama_chat tests
```

- Run type checking
```bash
mypy ollama_chat
```

### 5. Documentation
- Update API documentation if needed
- Add docstrings to new functions/classes
- Update README.md if adding features
- Update CHANGELOG.md

## Building and Packaging

### Desktop Application
```bash
python setup.py build
```

### Web Interface
```bash
cd web
npm run build
```

### Docker
```bash
docker-compose build
```

## Debugging

### Desktop Application
1. Use logging
```python
from ollama_chat.utils.logger import get_logger

logger = get_logger(__name__)
logger.debug("Debug message")
```

2. Use IPython for interactive debugging
```bash
ipython -i script.py
```

### Web Interface
1. Use Chrome DevTools
2. Use React Developer Tools
3. Check browser console for errors

## Common Issues and Solutions

### 1. Model Loading Issues
- Check Ollama server status
- Verify API endpoint configuration
- Check network connectivity

### 2. GUI Performance
- Use async operations for heavy tasks
- Implement proper error handling
- Monitor memory usage

### 3. Web Interface
- Check browser console for errors
- Verify API endpoints
- Check CORS configuration

## Performance Optimization

### Desktop Application
1. Profile code:
```bash
python -m cProfile -o output.prof script.py
```

2. Memory usage:
```bash
memory_profiler script.py
```

### Web Interface
1. Use React DevTools Profiler
2. Implement code splitting
3. Optimize bundle size

## Release Process

1. Version Bump
- Update version in setup.py
- Update CHANGELOG.md
- Create release notes

2. Testing
- Run full test suite
- Perform manual testing
- Check documentation

3. Build and Package
- Create distribution packages
- Test installation
- Update Docker images

4. Release
- Tag release in Git
- Create GitHub release
- Update documentation

## Additional Resources

- [Python Documentation](https://docs.python.org/3/)
- [React Documentation](https://reactjs.org/docs)
- [Ollama API Documentation](https://github.com/ollama/ollama)
- [customtkinter Documentation](https://customtkinter.tomschimansky.com/)
