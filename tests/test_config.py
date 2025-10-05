"""Tests for configuration management."""

import os
from unittest.mock import patch

import pytest

from fastmcp_ollama.config import Config, OllamaConfig, ServerConfig


class TestOllamaConfig:
    """Test OllamaConfig class."""

    def test_default_values(self):
        """Test default configuration values."""
        config = OllamaConfig()

        assert config.host == "http://127.0.0.1:11434"
        assert config.default_model is None
        assert config.request_timeout == 300
        assert config.max_retries == 3
        assert config.retry_delay == 1.0

    def test_environment_variables(self):
        """Test configuration from environment variables."""
        with patch.dict(os.environ, {
            "OLLAMA_HOST": "http://localhost:8080",
            "DEFAULT_MODEL": "llama2",
        }):
            config = OllamaConfig()

            assert config.host == "http://localhost:8080"
            assert config.default_model == "llama2"


class TestServerConfig:
    """Test ServerConfig class."""

    def test_default_values(self):
        """Test default server configuration values."""
        config = ServerConfig()

        assert config.name == "fastmcp-ollama"
        assert config.version == "0.1.0"
        assert config.description == "Advanced MCP server for Ollama"
        assert config.debug is False
        assert config.log_level == "INFO"

    def test_debug_from_environment(self):
        """Test debug configuration from environment."""
        with patch.dict(os.environ, {"DEBUG": "true"}):
            config = ServerConfig()
            assert config.debug is True

        with patch.dict(os.environ, {"DEBUG": "false"}):
            config = ServerConfig()
            assert config.debug is False

    def test_log_level_from_environment(self):
        """Test log level configuration from environment."""
        with patch.dict(os.environ, {"LOG_LEVEL": "DEBUG"}):
            config = ServerConfig()
            assert config.log_level == "DEBUG"


class TestConfig:
    """Test main Config class."""

    def test_from_env(self):
        """Test creating configuration from environment."""
        with patch.dict(os.environ, {
            "OLLAMA_HOST": "http://test:8080",
            "DEFAULT_MODEL": "test-model",
            "DEBUG": "true",
            "LOG_LEVEL": "DEBUG",
        }):
            config = Config.from_env()

            assert config.ollama.host == "http://test:8080"
            assert config.ollama.default_model == "test-model"
            assert config.server.debug is True
            assert config.server.log_level == "DEBUG"
