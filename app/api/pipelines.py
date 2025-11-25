from fastapi import APIRouter
from ..pipelines.example_pipeline import run_example_pipeline

router = APIRouter(prefix="/pipelines", tags=["pipelines"])


@router.post("/example-run")
async def trigger_example_pipeline():
    """
    Trigger the example pipeline.

    In real projects, you can:
    - Call this from a button in the UI.
    - Replace it with a scheduler / background task.
    """
    result = await run_example_pipeline()
    return result
