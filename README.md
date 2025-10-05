# FastMCP-Ollama

An advanced, extensible MCP (Model Context Protocol) server for Ollama, implemented with the FastMCP framework.

## Overview

FastMCP-Ollama provides a clean and modular implementation that exposes Ollama's capabilities through the MCP interface. It offers enhanced features beyond the basic reference implementation, including:

- **Modular Architecture**: Organized tool modules by functionality
- **Enhanced Configuration**: Flexible configuration management with environment variables
- **Robust Error Handling**: Comprehensive error handling and logging
- **Streaming Support**: Full streaming chat capabilities
- **Performance Optimization**: Connection pooling and retry mechanisms
- **Production Ready**: Docker support, health checks, and monitoring

## Features

### Core Tools

#### Model Management
- `list_models` - List all downloaded Ollama models
- `show_model` - Get detailed information about a specific model
- `pull_model` - Download a model from Ollama registry
- `remove_model` - Remove a downloaded model

#### Chat & Completion
- `chat` - Send chat messages with optional system prompts and context
- `chat_stream` - Streaming chat responses
- `chat_with_default_model` - Chat using the configured default model
- `generate_completion` - Generate text completions

#### Configuration & Information
- `get_config` - Show current server configuration
- `get_default_model` - Get the current default model name

## Installation

### From Source

```bash
git clone https://github.com/Wuodan/fastmcp-ollama.git
cd fastmcp-ollama
pip install -e .
```

### Using uv (recommended)

```bash
git clone https://github.com/Wuodan/fastmcp-ollama.git
cd fastmcp-ollama
uv sync
```

## Configuration

Configure the server using environment variables:

```bash
# Ollama server configuration
export OLLAMA_HOST="http://127.0.0.1:11434"
export DEFAULT_MODEL="llama2"

# Server configuration
export DEBUG="true"
export LOG_LEVEL="INFO"
```

### Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_HOST` | `http://127.0.0.1:11434` | Ollama server URL |
| `DEFAULT_MODEL` | `None` | Default model for chat operations |
| `DEBUG` | `false` | Enable debug logging |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Usage

### Running the Server

```bash
# Using the installed script
fastmcp-ollama

# Or run directly with Python
python -m fastmcp_ollama

# Or run the server module directly
python src/fastmcp_ollama/server.py
```

### Claude Desktop Configuration

Add to your Claude Desktop configuration file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "fastmcp-ollama": {
      "command": "uvx",
      "args": ["fastmcp-ollama"]
    }
  }
}
```

### Docker Usage

```bash
# Build the image
docker build -t fastmcp-ollama .

# Run with Docker
docker run -e OLLAMA_HOST=http://host.docker.internal:11434 fastmcp-ollama
```

## Development

### Prerequisites

- Python 3.10 or higher
- Ollama installed and running
- At least one model downloaded (e.g., `ollama pull llama2`)

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/Wuodan/fastmcp-ollama.git
cd fastmcp-ollama

# Install in development mode
pip install -e ".[dev]"

# Or using uv
uv sync --extra dev
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=fastmcp_ollama

# Run specific test file
pytest tests/test_config.py
```

### Code Quality

```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type checking
mypy src/
```

## Architecture

```
fastmcp-ollama/
├── src/fastmcp_ollama/
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # Entry point
│   ├── server.py            # Main MCP server
│   ├── config.py            # Configuration management
│   ├── utils.py             # Utility functions
│   └── tools/               # Tool modules
│       ├── __init__.py
│       ├── models.py        # Model management
│       └── chat.py          # Chat functionality
├── tests/                   # Test suite
├── docs/                    # Documentation
└── examples/               # Usage examples
```

## Comparison with Reference Implementation

| Feature | fastmcp-ollama | mcp-ollama |
|---------|----------------|------------|
| Architecture | Modular | Monolithic |
| Configuration | Pydantic-based | Environment only |
| Error Handling | Comprehensive | Basic |
| Streaming | Full support | Not available |
| Testing | Comprehensive | None |
| Docker | Supported | Not available |
| Tools | 10 tools | 5 tools |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- GitHub Issues: https://github.com/Wuodan/fastmcp-ollama/issues
- Documentation: https://github.com/Wuodan/fastmcp-ollama#readme

## Roadmap

- [ ] Enhanced multimodal support (vision, images)
- [ ] Embedding generation tools
- [ ] Model fine-tuning capabilities
- [ ] Advanced conversation management
- [ ] Plugin system for custom tools
- [ ] Web-based management interface
