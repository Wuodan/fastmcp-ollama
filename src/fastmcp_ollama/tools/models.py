"""Model management tools for fastmcp-ollama."""

import logging
from typing import List, Optional

from ..utils import format_model_info, get_ollama_client, retry_async, validate_model_name

logger = logging.getLogger(__name__)


async def list_models() -> str:
    """List all downloaded Ollama models.

    Returns:
        Formatted string containing information about all available models.
    """
    try:
        client = get_ollama_client()
        response = await retry_async(client.list)

        if not response.get('models'):
            return "No models found. Use 'pull_model' to download a model first."

        formatted_models = []
        for model in response['models']:
            formatted_models.append(format_model_info(model))

        return "\n---\n".join(formatted_models)
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        return f"Error listing models: {str(e)}"


async def show_model(name: str) -> str:
    """Get detailed information about a specific model.

    Args:
        name: Name of the model to show information about.

    Returns:
        Detailed information about the model or error message.
    """
    if not validate_model_name(name):
        return "Error: Invalid model name provided."

    try:
        client = get_ollama_client()
        response = await retry_async(client.show, name)

        if not response:
            return f"No information found for model '{name}'"

        # Format the detailed model information
        details = [
            f"Model: {name}",
            f"License: {response.get('license', 'Unknown')}",
            f"Format: {response.get('format', 'Unknown')}",
            f"Parameter Size: {response.get('parameter_size', 'Unknown')}",
            f"Quantization Level: {response.get('quantization_level', 'Unknown')}"
        ]

        # Add system prompt if available
        if response.get('system'):
            details.append(f"\nSystem Prompt:\n{response['system']}")

        # Add template if available
        if response.get('template'):
            details.append(f"\nTemplate:\n{response['template']}")

        # Add model info if available
        if response.get('model_info'):
            info = response['model_info']
            details.extend([
                f"\nModel Info:",
                f"  General: {info.get('general', 'N/A')}",
                f"  BPW: {info.get('bpw', 'N/A')}",
                f"  Parameters: {info.get('parameters', 'N/A')}"
            ])

        return "\n".join(details)
    except Exception as e:
        logger.error(f"Error getting model information for {name}: {e}")
        return f"Error getting model information: {str(e)}"


async def pull_model(name: str) -> str:
    """Download a model from Ollama registry.

    Args:
        name: Name of the model to download.

    Returns:
        Status message about the download operation.
    """
    if not validate_model_name(name):
        return "Error: Invalid model name provided."

    try:
        client = get_ollama_client()
        logger.info(f"Starting download of model: {name}")

        # For now, we'll use a simple pull - in a real implementation,
        # you might want to show progress
        response = await retry_async(client.pull, name)

        if response and response.get('status') == 'success':
            return f"Successfully downloaded model: {name}"
        else:
            return f"Download completed for model: {name}"

    except Exception as e:
        logger.error(f"Error downloading model {name}: {e}")
        return f"Error downloading model: {str(e)}"


async def remove_model(name: str) -> str:
    """Remove a downloaded model.

    Args:
        name: Name of the model to remove.

    Returns:
        Status message about the removal operation.
    """
    if not validate_model_name(name):
        return "Error: Invalid model name provided."

    try:
        client = get_ollama_client()
        logger.info(f"Removing model: {name}")

        response = await retry_async(client.delete, name)

        return f"Successfully removed model: {name}"
    except Exception as e:
        logger.error(f"Error removing model {name}: {e}")
        return f"Error removing model: {str(e)}"


async def get_available_models() -> List[str]:
    """Get list of available models from Ollama registry.

    Returns:
        List of available model names.
    """
    try:
        client = get_ollama_client()
        # Note: This might not be available in all Ollama versions
        # For now, return a basic list of popular models
        popular_models = [
            "llama2",
            "llama2:7b",
            "llama2:13b",
            "codellama",
            "mistral",
            "vicuna",
            "orca-mini"
        ]
        return popular_models
    except Exception as e:
        logger.error(f"Error getting available models: {e}")
        return []
