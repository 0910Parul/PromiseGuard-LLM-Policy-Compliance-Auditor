import time
from typing import Optional, Union

from ollama import Client

DEFAULT_MODEL = "llama3.1:8b"
DEFAULT_TIMEOUT = 180
MAX_RETRIES = 2
RETRY_BACKOFF_SECONDS = 2

_client = Client(timeout=DEFAULT_TIMEOUT)


def chat(
    prompt: str,
    *,
    system: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    format: Optional[Union[dict, str]] = None,
    temperature: float = 0.0,
) -> str:
    """Send a single-turn chat request to Ollama, retrying on transient failures."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    last_error: Optional[Exception] = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            response = _client.chat(
                model=model,
                messages=messages,
                format=format,
                options={"temperature": temperature},
            )
            return response["message"]["content"]
        except Exception as exc:
            last_error = exc
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_BACKOFF_SECONDS * (attempt + 1))

    raise RuntimeError(
        f"Ollama call to model '{model}' failed after {MAX_RETRIES + 1} attempts"
    ) from last_error
