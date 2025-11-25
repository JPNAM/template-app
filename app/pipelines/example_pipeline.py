import logging
from typing import Any

from ..integrations.example_public_api import ExamplePublicAPIClient

logger = logging.getLogger(__name__)


async def run_example_pipeline() -> dict[str, Any]:
    """
    Example pipeline that fetches data from an external API.

    AI tools:
    - Replace this with a real data pipeline.
    - Use it as a template for new pipeline functions.
    """
    client = ExamplePublicAPIClient()
    # Placeholder endpoint; AI will replace "/example" with real paths
    data = await client.fetch("/example", params={"limit": 10})
    logger.info("Fetched %s items from external API", len(data) if hasattr(data, "__len__") else "some")
    return {"fetched": data}
