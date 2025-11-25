from typing import Any
import httpx

from ..config import settings
from .base import ExternalDataClient


class ExamplePublicAPIClient(ExternalDataClient):
    """
    Template client for a third-party HTTP API.

    Replace EXTERNAL_API_BASE_URL / EXTERNAL_API_KEY with the real service
    in your .env file and extend this class.
    """

    def __init__(self) -> None:
        if not settings.EXTERNAL_API_BASE_URL:
            raise RuntimeError("EXTERNAL_API_BASE_URL is not set")
        self.base_url = settings.EXTERNAL_API_BASE_URL
        self.api_key = settings.EXTERNAL_API_KEY

    async def fetch(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:
        headers: dict[str, str] = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        async with httpx.AsyncClient(base_url=self.base_url, headers=headers, timeout=10) as client:
            resp = await client.get(endpoint, params=params)
            resp.raise_for_status()
            return resp.json()
