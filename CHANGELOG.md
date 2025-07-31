# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure and packaging configuration
- Comprehensive documentation and examples
- GitHub Actions CI/CD pipeline
- Pre-commit hooks for code quality
- Type hints and mypy configuration
- pytest test suite with coverage reporting

### Changed
- Restructured codebase into proper Python package layout
- Enhanced API documentation and examples

### Fixed
- N/A

## [0.1.0] - 2024-XX-XX

### Added
- Initial MCP server implementation for GLEIF API
- Support for all major GLEIF REST API endpoints:
  - LEI record search and retrieval
  - Fuzzy matching and auto-completion
  - LEI issuer information
  - Country and legal form reference data
  - API field metadata and filtering
- FastAPI-based server with automatic OpenAPI documentation
- Command-line interface for easy server startup
- Basic error handling and logging

### Features
- **LEI Records**: Complete CRUD operations for Legal Entity Identifiers
- **Search Capabilities**: Fuzzy matching, auto-completion, and advanced filtering
- **Reference Data**: Country codes, legal forms, and issuer information
- **Developer Tools**: Field metadata, pagination, and comprehensive error responses
- **MCP Protocol**: Full compliance with Model Context Protocol specification

### Technical Details
- Python 3.10+ support
- FastAPI web framework
- httpx for HTTP client operations
- Pydantic for data validation
- uvicorn for ASGI server

---

## Release Notes Format

Each release follows this structure:

### Added
- New features and capabilities

### Changed  
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Features removed in this version

### Fixed
- Bug fixes

### Security
- Vulnerability fixes and security improvements

---

## Versioning Strategy

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** version when you make incompatible API changes
- **MINOR** version when you add functionality in a backwards compatible manner  
- **PATCH** version when you make backwards compatible bug fixes

## Contributing to Changelog

When contributing:

1. Add your changes under the `[Unreleased]` section
2. Choose the appropriate category (Added, Changed, Fixed, etc.)
3. Use clear, concise descriptions
4. Reference GitHub issues/PRs when applicable
5. Follow the established format and style

## Links

- [Compare Unreleased Changes](https://github.com/GenAICPA/gleif-mcp-server/compare/v0.1.0...HEAD)
- [View All Releases](https://github.com/GenAICPA/gleif-mcp-server/releases)