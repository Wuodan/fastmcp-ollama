"""Configuration management for fastmcp-ollama."""

import os
from typing import Optional

from pydantic import BaseModel, Field


class OllamaConfig(BaseModel):
    """Configuration for Ollama connection."""

    host: str = Field(default_factory=lambda: os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434"))
    default_model: Optional[str] = Field(default_factory=lambda: os.getenv("DEFAULT_MODEL"))
    request_timeout: int = Field(default=300, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum number of retries")
    retry_delay: float = Field(default=1.0, description="Delay between retries in seconds")


class ServerConfig(BaseModel):
    """Configuration for the MCP server."""

    name: str = "fastmcp-ollama"
    version: str = "0.1.0"
    description: str = "Advanced MCP server for Ollama"
    debug: bool = Field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))


class Config(BaseModel):
    """Main configuration class."""

    ollama: OllamaConfig = Field(default_factory=OllamaConfig)
    server: ServerConfig = Field(default_factory=ServerConfig)

    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        return cls(
            ollama=OllamaConfig(),
            server=ServerConfig()
        )


# Global configuration instance
config = Config.from_env()
