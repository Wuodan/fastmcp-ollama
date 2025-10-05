"""FastMCP-Ollama: Advanced MCP server for Ollama integration."""

from .config import Config, config
from .server import run_server

__version__ = "0.1.0"
__all__ = ["Config", "config", "run_server"]
