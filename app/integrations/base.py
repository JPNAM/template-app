from abc import ABC, abstractmethod
from typing import Any


class ExternalDataClient(ABC):
    """
    Base class for external data clients.

    AI tools: subclass this when you integrate with a real API
    (e.g. Kalshi, FRED, Polygon, etc.).
    """

    @abstractmethod
    async def fetch(self, *args: Any, **kwargs: Any) -> Any:
        ...
