from pathlib import Path

FILES = {
    "README.md": """# template-app

Blank-but-ready template for new backend-style projects.

## Stack

- Python
- FastAPI
- Uvicorn
- Docker + docker-compose

## Quick start (for this template or any project created from it)

1. Clone the repo:
   git clone https://github.com/<your-username>/template-app.git
   cd template-app

2. Run the app:
   docker compose up --build

3. Open:

- API: http://localhost:8000
- API docs: http://localhost:8000/docs

You should see:

- /api/health endpoint returning {"status": "ok"}
- /api/example/items endpoint returning a stub list

## How to extend

- Add new endpoints in app/api/.
- Add business logic in app/services/.
- Define reusable domain models in app/models/.
- Use docs/ai-prompts.md for ready-made instructions to Codex / AI Studio / Antigravity to help you build features.
""",
    "requirements.txt": """fastapi
uvicorn[standard]
python-dotenv
""",
    ".env": """APP_NAME=Template App
APP_VERSION=0.1.0
DEBUG=true
""",
    "Dockerfile": """FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
""",
    "docker-compose.yml": """version: "3.9"

services:
  app:
    build: .
    container_name: template-app
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - ./app:/app/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
""",
    "app/__init__.py": """# Marks this directory as a Python package.
""",
    "app/config.py": """import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Template App")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"


settings = Settings()
""",
    "app/core/__init__.py": """# Core utilities (logging, etc.) live here.
""",
    "app/core/logging.py": """import logging


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
""",
    "app/api/__init__.py": """# API routers live here (health, example, and any new ones you add).
""",
    "app/api/health.py": """from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    return {"status": "ok"}
""",
    "app/api/example.py": """from fastapi import APIRouter
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
""",
    "app/models/__init__.py": """# Define reusable domain models here when your project needs them.
""",
    "app/services/__init__.py": """# Implement business logic / services here.
# For example: database queries, external API calls, calculations, etc.
""",
    "app/main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .core.logging import configure_logging
from .api import health, example


configure_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(example.router, prefix="/api")
""",
    "docs/ai-prompts.md": """# AI Prompts

This repo is a blank-but-ready FastAPI + Docker template.

Use this file as a starting point when asking Codex / ChatGPT / Gemini / Antigravity agents to extend the app.

## Add a new resource (example prompt)

You are working in a FastAPI project using this structure:
- app/main.py is the FastAPI entrypoint.
- app/api/ contains routers.
- app/services/ contains business logic.
- app/models/ will contain domain models.

Please:
1. Create a new router in app/api/users.py with CRUD endpoints for a User resource.
2. Define a Pydantic model User in that file with fields: id (int), email (str), name (str | None).
3. Use an in-memory list as a stand-in for persistence, similar to app/api/example.py.
4. Register the new router in app/main.py under the prefix /api.

Return the full contents of any new or changed files.

## Add database support later

I am using the same template-app structure as before.
I now want to add a PostgreSQL database using SQLAlchemy.

Please:
1. Add a dependency on SQLAlchemy to requirements.txt.
2. Create app/models/base.py with a SQLAlchemy Base.
3. Create a simple User ORM model.
4. Show how to configure the database URL from an environment variable in app/config.py.
5. Update app/services/users_service.py to read/write users from the database instead of the in-memory list.
"""
}


def main():
    for path, content in FILES.items():
        p = Path(path)
        if not p.parent.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
        if p.exists():
            print(f"Skipping existing {p}")
            continue
        p.write_text(content, encoding="utf-8")
        print(f"Created {p}")


if __name__ == "__main__":
    main()
