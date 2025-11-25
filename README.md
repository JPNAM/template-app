# template-app

Blank-but-ready backend template with a small, opinionated structure so humans and LLMs can extend it safely.

* Single FastAPI service
* Docker-first: `docker compose up --build` to run anywhere
* Clear places for:

  * API endpoints
  * Business logic / services
  * External data integrations (HTTP APIs, etc.)
  * Data pipelines / jobs

## Stack

* Python 3
* FastAPI
* Uvicorn
* Docker + Docker Compose
* `python-dotenv` for configuration via `.env`
* `httpx` for HTTP integrations (async)

---

## Quick start

For this template or any project created from it:

1. Clone the repo:

   ```bash
   git clone https://github.com/<your-username>/template-app.git
   cd template-app
   ```

2. Run the app:

   ```bash
   docker compose up --build
   ```

3. Open in your browser:

   * API root: [http://localhost:8000/](http://localhost:8000/)
   * API docs (Swagger UI): [http://localhost:8000/docs](http://localhost:8000/docs)

You should see:

* `GET /api/health` returning `{"status": "ok"}`
* `GET /api/example/items` returning a stub list of items

Stop the app with `Ctrl + C` in the terminal.

---

## Configuration

Configuration is done via `.env` (loaded by `python-dotenv`).

Default `.env`:

```env
APP_NAME=Template App
APP_VERSION=0.1.0
DEBUG=true

EXTERNAL_API_BASE_URL=
EXTERNAL_API_KEY=
```

These values are exposed in `app/config.py` via the `settings` object and can be used anywhere in the app.

---

## Project layout

High-level structure:

```text
template-app/
  Dockerfile
  docker-compose.yml
  requirements.txt
  .env
  app/
    __init__.py
    main.py
    config.py
    core/
      __init__.py
      logging.py
    api/
      __init__.py
      health.py
      example.py
      # (optional) pipelines.py, users.py, etc.
    integrations/
      __init__.py
      base.py
      example_public_api.py
    pipelines/
      __init__.py
      # (optional) example_pipeline.py, other pipelines
    models/
      __init__.py
    services/
      __init__.py
  docs/
    ai-prompts.md
```

### `app/main.py`

* Creates the FastAPI app.
* Configures CORS.
* Registers routers under `/api`.
* Optionally defines a simple root `GET /` endpoint for a status message.

### `app/api/`

All HTTP API endpoints (routers) live here.

Existing routers:

* `health.py` → `GET /api/health`
* `example.py` → `GET /api/example/items`, `POST /api/example/items`

New resources (e.g. `users`, `orders`, `metrics`) should be added as new files here and registered in `main.py`.

### `app/core/`

Cross-cutting concerns:

* `logging.py` – `configure_logging()` sets up basic logging.

### `app/config.py`

* Loads environment variables from `.env`.
* Provides a `Settings` dataclass instance (`settings`) used across the app.
* Holds fields such as:

  * `APP_NAME`, `APP_VERSION`, `DEBUG`
  * `EXTERNAL_API_BASE_URL`, `EXTERNAL_API_KEY` (for external APIs)

### `app/integrations/`

External API clients live here (HTTP APIs, vendor SDK wrappers, etc.).

* `base.py` – `ExternalDataClient` abstract base class.
* `example_public_api.py` – template `ExamplePublicAPIClient` using `httpx.AsyncClient` and `settings`.

When integrating a real external API, add a new client file here and configure it via `.env` + `Settings`.

### `app/pipelines/`

Data pipelines / jobs (fetch → transform → return/store) live here.

Typical use:

* A pipeline module orchestrates one or more integration clients.
* Pipelines can be triggered by:

  * API endpoints in `app/api/`
  * Background tasks
  * Schedulers / external runners

### `app/models/`

Domain / shared Pydantic models live here (currently empty).

### `app/services/`

Business logic services live here (e.g. “user service”, “pricing service”).

Routers in `app/api/` should be kept thin and delegate non-trivial logic to services.

### `docs/ai-prompts.md`

Contains reusable prompt snippets for Codex / ChatGPT / Gemini / Antigravity, showing how to:

* Add new routers/endpoints.
* Build integrations and pipelines.
* Wire new pieces into this structure.

---

## How to extend

### 1. Add a new resource / endpoint

Where to put code:

* Router: `app/api/<resource>.py`
* Optional service logic: `app/services/<resource>_service.py`
* Optional shared models: `app/models/<resource>.py`

Basic steps:

1. Create `app/api/users.py` with a FastAPI `APIRouter` and CRUD endpoints.

2. Register it in `app/main.py`:

   ```python
   from .api import health, example, users  # add users

   # ...
   app.include_router(health.router, prefix="/api")
   app.include_router(example.router, prefix="/api")
   app.include_router(users.router, prefix="/api")
   ```

3. Run `docker compose up` and verify new endpoints in `/docs`.

### 2. Add an external data integration

Where to put code:

* Client: `app/integrations/<provider>_client.py`
* Config: new env vars in `.env` + fields in `Settings`.
* Optional pipeline: `app/pipelines/<provider>_pipeline.py`.

Typical flow:

1. Add env vars in `.env`, e.g.:

   ```env
   PROVIDER_BASE_URL=...
   PROVIDER_API_KEY=...
   ```

2. Add corresponding fields to `Settings` in `app/config.py`.

3. Implement a client class in `app/integrations/provider_client.py` that:

   * Subclasses `ExternalDataClient`.
   * Uses `httpx.AsyncClient`.
   * Reads config from `settings`.

4. Use this client from a pipeline or directly from an API route.

### 3. Add a data pipeline

Where to put code:

* Pipeline module: `app/pipelines/<name>_pipeline.py`.
* Optional trigger endpoint: `app/api/pipelines.py` (e.g. `POST /api/pipelines/<name>-run`).

Typical flow:

1. Write a function in `app/pipelines/<name>_pipeline.py` that:

   * Instantiates integration clients.
   * Fetches external data.
   * Transforms it into Pydantic models or dicts.
   * Returns or persists the result.

2. Add a route in `app/api/pipelines.py` that calls this function.

3. Register the pipelines router in `app/main.py`.

---

## Using this template with LLMs

When prompting Codex / ChatGPT / Gemini / Antigravity to modify this project, include a short description of the structure, for example:

> You are modifying a FastAPI project with this structure:
>
> * `app/main.py`: FastAPI app and router registration.
> * `app/api/`: HTTP routers.
> * `app/services/`: business logic.
> * `app/integrations/`: external API clients using `httpx`.
> * `app/pipelines/`: data pipelines orchestrating integrations.
> * `app/config.py`: configuration via a `Settings` object reading `.env`.
>   Please keep new code aligned with this structure and use `app.config.settings` for configuration instead of hard-coded constants.

For concrete prompt templates, see `docs/ai-prompts.md`.
