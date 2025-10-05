"""Main MCP server implementation for fastmcp-ollama."""

import logging
from typing import Any, Dict

from mcp.server.fastmcp import FastMCP

from .config import config
from .tools import (
    chat,
    chat_stream,
    chat_with_default_model,
    generate_completion,
    list_models,
    pull_model,
    remove_model,
    show_model,
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.server.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP(
    name=config.server.name,
    description=config.server.description,
    dependencies=["ollama", "pydantic"]
)


@mcp.tool()
async def list_models_tool() -> str:
    """List all downloaded Ollama models.

    Returns:
        Formatted string containing information about all available models.
    """
    return await list_models()


@mcp.tool()
async def show_model_tool(name: str) -> str:
    """Get detailed information about a specific model.

    Args:
        name: Name of the model to show information about.

    Returns:
        Detailed information about the model or error message.
    """
    return await show_model(name)


@mcp.tool()
async def pull_model_tool(name: str) -> str:
    """Download a model from Ollama registry.

    Args:
        name: Name of the model to download.

    Returns:
        Status message about the download operation.
    """
    return await pull_model(name)


@mcp.tool()
async def remove_model_tool(name: str) -> str:
    """Remove a downloaded model.

    Args:
        name: Name of the model to remove.

    Returns:
        Status message about the removal operation.
    """
    return await remove_model(name)


@mcp.tool()
async def chat_tool(
    model: str,
    message: str,
    system_prompt: str = None,
    context: str = None
) -> str:
    """Send a chat message to a model and get response.

    Args:
        model: Name of the model to use.
        message: The message to send.
        system_prompt: Optional system prompt to set context.
        context: Optional conversation context as JSON string.

    Returns:
        Model response or error message.
    """
    # Parse context if provided
    parsed_context = None
    if context:
        try:
            parsed_context = eval(context)  # Simple parsing - could use json in production
        except:
            pass

    return await chat(
        model=model,
        message=message,
        system_prompt=system_prompt,
        context=parsed_context
    )


@mcp.tool()
async def chat_stream_tool(
    model: str,
    message: str,
    system_prompt: str = None,
    context: str = None
) -> str:
    """Send a chat message with streaming response.

    Args:
        model: Name of the model to use.
        message: The message to send.
        system_prompt: Optional system prompt to set context.
        context: Optional conversation context as JSON string.

    Returns:
        Complete model response (streaming chunks combined).
    """
    # Parse context if provided
    parsed_context = None
    if context:
        try:
            parsed_context = eval(context)  # Simple parsing - could use json in production
        except:
            pass

    # Collect streaming response
    response_chunks = []
    async for chunk in chat_stream(
        model=model,
        message=message,
        system_prompt=system_prompt,
        context=parsed_context
    ):
        response_chunks.append(chunk)

    return "".join(response_chunks)


@mcp.tool()
async def chat_with_default_model_tool(
    message: str,
    system_prompt: str = None,
    context: str = None
) -> str:
    """Chat with the default model configured in environment.

    Args:
        message: The message to send.
        system_prompt: Optional system prompt to set context.
        context: Optional conversation context as JSON string.

    Returns:
        Model response or error message.
    """
    # Parse context if provided
    parsed_context = None
    if context:
        try:
            parsed_context = eval(context)  # Simple parsing - could use json in production
        except:
            pass

    return await chat_with_default_model(
        message=message,
        system_prompt=system_prompt,
        context=parsed_context
    )


@mcp.tool()
async def generate_completion_tool(
    model: str,
    prompt: str,
    suffix: str = None,
    system_prompt: str = None
) -> str:
    """Generate a completion using a model.

    Args:
        model: Name of the model to use.
        prompt: The prompt to complete.
        suffix: Optional suffix to append to completion.
        system_prompt: Optional system prompt.

    Returns:
        Generated completion or error message.
    """
    return await generate_completion(
        model=model,
        prompt=prompt,
        suffix=suffix,
        system_prompt=system_prompt
    )


@mcp.tool()
async def get_config_tool() -> str:
    """Get current server configuration.

    Returns:
        Formatted configuration information.
    """
    return f"""Server Configuration:
Name: {config.server.name}
Version: {config.server.version}
Description: {config.server.description}
Debug: {config.server.debug}
Log Level: {config.server.log_level}

Ollama Configuration:
Host: {config.ollama.host}
Default Model: {config.ollama.default_model or 'Not configured'}
Request Timeout: {config.ollama.request_timeout}s
Max Retries: {config.ollama.max_retries}
Retry Delay: {config.ollama.retry_delay}s
"""


@mcp.tool()
async def get_default_model_tool() -> str:
    """Get the current default model name.

    Returns:
        Default model name or error message.
    """
    if not config.ollama.default_model:
        return "No default model configured. Set DEFAULT_MODEL environment variable."
    return config.ollama.default_model


def run_server() -> None:
    """Run the MCP server using stdio transport."""
    logger.info(f"Starting {config.server.name} v{config.server.version}")
    logger.info(f"Ollama host: {config.ollama.host}")
    logger.info(f"Default model: {config.ollama.default_model or 'Not configured'}")

    mcp.run(transport='stdio')


if __name__ == "__main__":
    run_server()
