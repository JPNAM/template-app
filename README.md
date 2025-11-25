# template-app

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
