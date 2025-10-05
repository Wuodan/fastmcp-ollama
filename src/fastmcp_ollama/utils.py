"""Utility functions for fastmcp-ollama."""

import asyncio
import logging
from typing import Any, Dict, Optional, TypeVar

from ollama import Client

from .config import config

T = TypeVar('T')

logger = logging.getLogger(__name__)


def get_ollama_client() -> Client:
    """Get configured Ollama client."""
    return Client(
        host=config.ollama.host,
        timeout=config.ollama.request_timeout
    )


async def retry_async(
    func: callable,
    *args,
    max_retries: Optional[int] = None,
    retry_delay: Optional[float] = None,
    **kwargs
) -> Any:
    """Retry an async function with exponential backoff."""
    if max_retries is None:
        max_retries = config.ollama.max_retries
    if retry_delay is None:
        retry_delay = config.ollama.retry_delay

    last_exception = None

    for attempt in range(max_retries + 1):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt < max_retries:
                wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                logger.warning(
                    f"Attempt {attempt + 1} failed: {e}. Retrying in {wait_time}s..."
                )
                await asyncio.sleep(wait_time)
            else:
                logger.error(f"All {max_retries + 1} attempts failed. Last error: {e}")

    raise last_exception


def format_model_info(model_data: Dict[str, Any]) -> str:
    """Format model information for display."""
    lines = [
        f"Name: {model_data.get('model', 'Unknown')}",
        f"Size: {model_data.get('size', 'Unknown')}",
        f"Modified: {model_data.get('modified_at', 'Unknown')}"
    ]

    # Add additional details if available
    if 'details' in model_data:
        details = model_data['details']
        lines.extend([
            f"Format: {details.get('format', 'Unknown')}",
            f"Parameter Size: {details.get('parameter_size', 'Unknown')}",
            f"Quantization Level: {details.get('quantization_level', 'Unknown')}"
        ])

    return "\n".join(lines)


def validate_model_name(model_name: str) -> bool:
    """Validate model name format."""
    if not model_name or not isinstance(model_name, str):
        return False
    # Basic validation - can be extended
    return len(model_name.strip()) > 0


def sanitize_input(text: str, max_length: int = 10000) -> str:
    """Sanitize user input."""
    if not isinstance(text, str):
        return ""
    return text.strip()[:max_length]
