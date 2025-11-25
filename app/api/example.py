from fastapi import APIRouter
from pydantic import BaseModel
from typing import List


router = APIRouter(prefix="/example", tags=["example"])


class Item(BaseModel):
    id: int
    name: str
    description: str | None = None


_FAKE_DB: list[Item] = [
    Item(id=1, name="Sample item", description="Replace me with your own model"),
]


@router.get("/items", response_model=List[Item])
def list_items():
    return _FAKE_DB


@router.post("/items", response_model=Item)
def create_item(item: Item):
    _FAKE_DB.append(item)
    return item
