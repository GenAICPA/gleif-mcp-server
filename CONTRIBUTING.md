# Contributing to GLEIF MCP Server

Thank you for your interest in contributing to the GLEIF MCP Server! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Submitting Changes](#submitting-changes)
- [Release Process](#release-process)

## Code of Conduct

This project adheres to the Contributor Covenant [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- GitHub account

### Types of Contributions

We welcome several types of contributions:

- 🐛 **Bug Reports**: Help us identify and fix issues
- 💡 **Feature Requests**: Suggest new functionality
- 📝 **Documentation**: Improve or add documentation
- 🔧 **Code Contributions**: Bug fixes, features, optimizations
- 🧪 **Testing**: Add or improve test coverage
- 🎨 **Examples**: Add usage examples and tutorials

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/gleif-mcp-server.git
cd gleif-mcp-server

# Add the original repository as upstream
git remote add upstream https://github.com/GenAICPA/gleif-mcp-server.git
```

### 2. Create Development Environment

```bash
# Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package in development mode with all dependencies
pip install -e ".[dev,test,docs]"

# Install pre-commit hooks
pre-commit install
```

### 3. Verify Setup

```bash
# Run tests to ensure everything works
pytest

# Check code formatting and linting
pre-commit run --all-files

# Start the server to test functionality
gleif-mcp-server
```

## Making Changes

### 1. Create a Branch

```bash
# Keep your main branch clean and create feature branches
git checkout main
git pull upstream main
git checkout -b feature/your-feature-name
```

### 2. Branch Naming Convention

Use descriptive branch names:
- `feature/add-new-endpoint` - for new features
- `bugfix/fix-connection-error` - for bug fixes  
- `docs/update-readme` - for documentation changes
- `refactor/improve-error-handling` - for code improvements

### 3. Commit Messages

Follow conventional commit format:

```
type(scope): brief description

Longer description if needed

Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat(api): add fuzzy search endpoint`
- `fix(client): handle connection timeout properly`
- `docs(readme): update installation instructions`

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gleif_mcp --cov-report=html

# Run specific test categories
pytest -m "not live"  # Skip live API tests
pytest -m integration  # Run only integration tests
pytest tests/test_server.py  # Run specific test file
```

### Writing Tests

- Add tests for new features in `tests/`
- Use descriptive test names: `test_get_lei_record_returns_valid_data`
- Mock external API calls for unit tests
- Mark live API tests with `@pytest.mark.live`
- Aim for >80% code coverage

### Test Categories

- **Unit Tests**: Test individual functions/methods
- **Integration Tests**: Test component interactions  
- **Live Tests**: Test against real GLEIF API (use sparingly)

## Code Style

We use automated code formatting and linting:

### Tools Used

- **Black**: Code formatting (line length: 88)
- **Ruff**: Fast Python linter and formatter
- **isort**: Import sorting
- **mypy**: Type checking
- **bandit**: Security scanning

### Pre-commit Hooks

Pre-commit hooks automatically run before each commit:

```bash
# Run manually on all files
pre-commit run --all-files

# Skip hooks for emergency commits (not recommended)
git commit --no-verify -m "emergency fix"
```

### Type Hints

- Use type hints for all public APIs
- Import types from `typing` or `collections.abc`
- Use `Protocol` for duck-typed interfaces

```python
from typing import Dict, List, Optional, Union
from collections.abc import AsyncIterator

def search_records(query: str, limit: Optional[int] = None) -> Dict[str, Any]:
    ...
```

## Submitting Changes

### 1. Before Submitting

- [ ] Tests pass locally (`pytest`)
- [ ] Code passes all pre-commit checks
- [ ] Documentation is updated if needed
- [ ] CHANGELOG.md is updated (add to Unreleased section)
- [ ] Commit messages follow conventional format

### 2. Create Pull Request

1. Push your branch to your fork
2. Open a Pull Request on GitHub
3. Fill out the PR template completely
4. Link any related issues

### 3. PR Requirements

- Clear description of changes
- Passing CI checks
- At least one approving review
- Up-to-date with main branch

### 4. Review Process

- Maintainers will review within 1-2 business days
- Address feedback promptly
- Keep discussions respectful and constructive
- Be prepared to iterate on your changes

## Documentation

### Types of Documentation

- **Code Comments**: Explain complex logic
- **Docstrings**: Document public APIs (use Google style)
- **README**: Keep up-to-date with features
- **Examples**: Add practical usage examples
- **API Docs**: Update OpenAPI specs if needed

### Documentation Style

```python
def search_lei_records(query: str, limit: int = 10) -> Dict[str, Any]:
    """Search for LEI records matching the query.
    
    Args:
        query: Search term to match against entity names
        limit: Maximum number of results to return
        
    Returns:
        Dictionary containing search results and metadata
        
    Raises:
        HTTPException: If the GLEIF API request fails
        
    Example:
        >>> results = search_lei_records("Apple Inc", limit=5)
        >>> print(f"Found {len(results['data'])} entities")
    """
```

## Release Process

### For Maintainers

1. **Prepare Release**
   - Update version in `gleif_mcp/__init__.py`
   - Move unreleased changes in CHANGELOG.md to new version
   - Update documentation if needed

2. **Create Release**
   - Create and push version tag: `git tag v1.2.3`
   - GitHub Actions will automatically build and publish to PyPI
   - Create GitHub Release from tag with changelog notes

3. **Post-Release**
   - Announce release in discussions/README
   - Update any dependent projects

## Getting Help

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Pull Request Comments**: Code-specific discussions

### Common Questions

**Q: How do I test against the live GLEIF API?**
A: Use `pytest -m live` to run live tests. Be mindful of rate limits.

**Q: Can I add a new GLEIF API endpoint?**
A: Yes! Follow the existing patterns in `server.py` and add comprehensive tests.

**Q: How do I handle breaking changes?**
A: Discuss breaking changes in an issue first. They require a major version bump.

## Recognition

Contributors are recognized in several ways:
- Listed in GitHub contributors
- Mentioned in release notes for significant contributions  
- Added to AUTHORS file for major contributions

Thank you for contributing to the GLEIF MCP Server! 🎉