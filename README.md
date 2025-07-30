# GLEIF MCP Server

[![CI](https://github.com/GenAICPA/gleif-mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/GenAICPA/gleif-mcp-server/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/gleif-mcp-server.svg)](https://badge.fury.io/py/gleif-mcp-server)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Model Context Protocol (MCP) server that provides seamless access to the GLEIF (Global Legal Entity Identifier Foundation) REST API. This server enables AI assistants and other MCP-compatible applications to query legal entity information, including LEI records, issuer details, and hierarchical relationships between organizations.

## Features

### 🔍 **LEI Record Management**
- **Search & Retrieve**: Find LEI records by various criteria (legal name, LEI code, jurisdiction)
- **Fuzzy Matching**: Approximate search with auto-completion for entity discovery
- **Live Data**: Real-time access to the most current GLEIF database

### 🏢 **Entity Information** 
- **Legal Entity Details**: Complete legal name, jurisdiction, status, and registration info
- **Address Data**: Headquarters and legal addresses with full geographical details
- **Entity Relationships**: Parent-subsidiary relationships and ownership structures

### 🌍 **Reference Data**
- **Country Codes**: ISO 3166 country code lookups and validation  
- **Legal Forms**: Entity Legal Form (ELF) code reference data
- **Issuer Network**: Information about LEI issuing organizations (LOUs)

### 🔧 **Developer Tools**
- **Field Metadata**: Comprehensive API field documentation and filtering capabilities
- **Pagination**: Efficient handling of large result sets
- **Type Safety**: Full Python type hints and Pydantic validation

## Quick Start

### Installation

```bash
pip install gleif-mcp-server
```

### Start the MCP Server

```bash
# Start server on default port (8000)
gleif-mcp-server

# Or specify custom port
gleif-mcp-server --port 8080
```

### Use as Python Client

```python
from gleif_mcp import client

# Get specific LEI record
lei_data = client.get_lei_record("529900T8BM49AURSDO55")
print(f"Entity: {lei_data['entity']['legalName']}")

# Search for entities
results = client.search_lei_records("entity.legalName", "Citibank")
for record in results['data']:
    print(f"Found: {record['entity']['legalName']}")

# Fuzzy search with suggestions
suggestions = client.fuzzy_completions("entity.legalName", "Apple Inc")
```

## MCP Integration

This server is compatible with any MCP client, including:

- **Claude Desktop**: Add to your `claude_desktop_config.json`
- **Cline/Windsurf**: Configure as an MCP server
- **Custom Applications**: Use the standard MCP protocol

### Configuration Example

```json
{
  "mcpServers": {
    "gleif": {
      "command": "gleif-mcp-server",
      "args": []
    }
  }
}
```

## API Coverage

The server provides access to all major GLEIF API endpoints:

| **Category** | **Endpoint** | **Description** |
|--------------|--------------|-----------------|
| **LEI Records** | `/lei-records` | Search and retrieve LEI records |
| **LEI Records** | `/lei-records/{lei}` | Get specific LEI record by code |
| **Search** | `/lei-records/fuzzy-completions` | Fuzzy matching for entity names |
| **Search** | `/lei-records/auto-completions` | Auto-complete suggestions |
| **Issuers** | `/lei-issuers` | List accredited LEI issuers |
| **Issuers** | `/lei-issuers/{id}` | Get specific issuer details |
| **Reference** | `/countries` | ISO 3166 country codes |
| **Reference** | `/entity-legal-forms` | ELF codes and descriptions |
| **Metadata** | `/fields` | API field catalog and filtering options |

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/GenAICPA/gleif-mcp-server.git
cd gleif-mcp-server

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Run Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=gleif_mcp

# Skip live API tests (for CI)
pytest -m "not live"

# Run only integration tests
pytest -m integration
```

### Code Quality

```bash
# Format code
black gleif_mcp tests

# Lint code  
ruff check gleif_mcp tests

# Type checking
mypy gleif_mcp
```

## Examples

### Find Entity by Name

```python
# Search for entities containing "Microsoft"
results = client.search_lei_records("entity.legalName", "*Microsoft*")

for entity in results['data'][:5]:  # Show first 5 results
    print(f"LEI: {entity['lei']}")
    print(f"Name: {entity['entity']['legalName']}")
    print(f"Country: {entity['entity']['jurisdiction']}")
    print("---")
```

### Get Entity Hierarchy

```python
# Get parent company information
lei = "529900T8BM49AURSDO55"  # Example LEI
record = client.get_lei_record(lei)

if record['entity'].get('parent'):
    parent_lei = record['entity']['parent']['lei'] 
    parent_data = client.get_lei_record(parent_lei)
    print(f"Parent: {parent_data['entity']['legalName']}")
```

### Country and Legal Form Lookup

```python
# Get country information
country = client.get_country("US")
print(f"Country: {country['name']} ({country['code']})")

# List available legal forms
legal_forms = client.list_entity_legal_forms()
for form in legal_forms['data'][:10]:
    print(f"{form['code']}: {form['name']}")
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Ensure all tests pass and code is formatted
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [GLEIF](https://www.gleif.org/) for providing the comprehensive LEI database and API
- [Model Context Protocol](https://modelcontextprotocol.io/) for the standard protocol specification
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework

## Support

- 📖 [Documentation](https://github.com/GenAICPA/gleif-mcp-server#readme)
- 🐛 [Report Issues](https://github.com/GenAICPA/gleif-mcp-server/issues)  
- 💬 [Discussions](https://github.com/GenAICPA/gleif-mcp-server/discussions)

---

**Note**: This is an unofficial implementation. GLEIF does not endorse or maintain this server.