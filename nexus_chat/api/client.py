import httpx
from typing import AsyncGenerator, Optional
from functools import wraps
from httpx import HTTPStatusError, RequestError
import logging

logger = logging.getLogger(__name__)

class APIError(Exception):
    pass

def handle_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPStatusError as e:
            logger.error(f"API Error: {e.response.status_code} - {e.response.text}")
            raise APIError(f"API request failed: {e.response.status_code}") from e
        except RequestError as e:
            logger.error(f"Connection Error: {str(e)}")
            raise APIError("Connection to Ollama API failed") from e
    return wrapper

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.client = httpx.AsyncClient(base_url=base_url)
        self._models: Optional[list] = None

    @handle_errors
    async def list_models(self) -> list:
        response = await self.client.get("/api/tags")
        return response.json().get("models", [])

    @handle_errors
    async def generate(self, model: str, prompt: str) -> AsyncGenerator[str, None]:
        if not await self.model_exists(model):
            raise APIError(f"Model {model} not found")

        async with self.client.stream(
            "POST",
            "/api/generate",
            json={"model": model, "prompt": prompt, "stream": True}
        ) as response:
            response.raise_for_status()
            async for chunk in response.aiter_json():
                yield chunk.get("response", "")

    async def model_exists(self, model: str) -> bool:
        if not self._models:
            self._models = await self.list_models()
        return any(m["name"] == model for m in self._models)

    async def close(self):
        await self.client.aclose()
