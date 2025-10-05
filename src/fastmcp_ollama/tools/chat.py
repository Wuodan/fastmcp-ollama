"""Chat and completion tools for fastmcp-ollama."""

import logging
from typing import AsyncGenerator, List, Optional

from ..config import config
from ..utils import get_ollama_client, retry_async, sanitize_input, validate_model_name

logger = logging.getLogger(__name__)


async def chat(
    model: str,
    message: str,
    system_prompt: Optional[str] = None,
    context: Optional[List[dict]] = None
) -> str:
    """Send a chat message to a model and get response.

    Args:
        model: Name of the model to use.
        message: The message to send.
        system_prompt: Optional system prompt to set context.
        context: Optional conversation context.

    Returns:
        Model response or error message.
    """
    if not validate_model_name(model):
        return "Error: Invalid model name provided."

    message = sanitize_input(message)
    if not message:
        return "Error: Empty message provided."

    try:
        client = get_ollama_client()
        messages = []

        # Add system prompt if provided
        if system_prompt:
            system_prompt = sanitize_input(system_prompt, max_length=5000)
            messages.append({
                'role': 'system',
                'content': system_prompt
            })

        # Add conversation context if provided
        if context:
            messages.extend(context)

        # Add user message
        messages.append({
            'role': 'user',
            'content': message
        })

        logger.info(f"Sending chat message to model: {model}")

        response = await retry_async(
            client.chat,
            model=model,
            messages=messages
        )

        if response and 'message' in response:
            return response['message']['content']
        else:
            return "Error: No response received from model"

    except Exception as e:
        logger.error(f"Error in chat with model {model}: {e}")
        return f"Error communicating with model: {str(e)}"


async def chat_stream(
    model: str,
    message: str,
    system_prompt: Optional[str] = None,
    context: Optional[List[dict]] = None
) -> AsyncGenerator[str, None]:
    """Send a chat message with streaming response.

    Args:
        model: Name of the model to use.
        message: The message to send.
        system_prompt: Optional system prompt to set context.
        context: Optional conversation context.

    Yields:
        Chunks of the model response as they arrive.
    """
    if not validate_model_name(model):
        yield "Error: Invalid model name provided."
        return

    message = sanitize_input(message)
    if not message:
        yield "Error: Empty message provided."
        return

    try:
        client = get_ollama_client()
        messages = []

        # Add system prompt if provided
        if system_prompt:
            system_prompt = sanitize_input(system_prompt, max_length=5000)
            messages.append({
                'role': 'system',
                'content': system_prompt
            })

        # Add conversation context if provided
        if context:
            messages.extend(context)

        # Add user message
        messages.append({
            'role': 'user',
            'content': message
        })

        logger.info(f"Sending streaming chat message to model: {model}")

        # Use streaming response
        async for chunk in await client.chat(
            model=model,
            messages=messages,
            stream=True
        ):
            if chunk and 'message' in chunk and 'content' in chunk['message']:
                yield chunk['message']['content']

    except Exception as e:
        logger.error(f"Error in streaming chat with model {model}: {e}")
        yield f"Error communicating with model: {str(e)}"


async def chat_with_default_model(
    message: str,
    system_prompt: Optional[str] = None,
    context: Optional[List[dict]] = None
) -> str:
    """Chat with the default model configured in environment.

    Args:
        message: The message to send.
        system_prompt: Optional system prompt to set context.
        context: Optional conversation context.

    Returns:
        Model response or error message.
    """
    if not config.ollama.default_model:
        return "Error: No default model configured. Set DEFAULT_MODEL environment variable."

    return await chat(
        model=config.ollama.default_model,
        message=message,
        system_prompt=system_prompt,
        context=context
    )


async def generate_completion(
    model: str,
    prompt: str,
    suffix: Optional[str] = None,
    system_prompt: Optional[str] = None
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
    if not validate_model_name(model):
        return "Error: Invalid model name provided."

    prompt = sanitize_input(prompt)
    if not prompt:
        return "Error: Empty prompt provided."

    try:
        client = get_ollama_client()

        # Build the full prompt
        full_prompt = prompt
        if system_prompt:
            system_prompt = sanitize_input(system_prompt, max_length=5000)
            full_prompt = f"{system_prompt}\n\n{prompt}"

        options = {}
        if suffix:
            suffix = sanitize_input(suffix, max_length=1000)
            options['suffix'] = suffix

        logger.info(f"Generating completion with model: {model}")

        response = await retry_async(
            client.generate,
            model=model,
            prompt=full_prompt,
            options=options
        )

        if response and 'response' in response:
            return response['response']
        else:
            return "Error: No response received from model"

    except Exception as e:
        logger.error(f"Error generating completion with model {model}: {e}")
        return f"Error generating completion: {str(e)}"
