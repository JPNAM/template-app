# AI Prompts

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

## Build a live data pipeline

You are working in this template-app:

- External API clients live in app/integrations/.
- Pipelines live in app/pipelines/.
- Environment variables are read from app/config.py.

Please:

1. # Implement a client for the <NAME> API in app/integrations <name>_client.py.
   - # Use httpx.AsyncClient.
   - # Read base URL and API key from new env vars (document them).
2. # Implement a pipeline function in app/pipelines/<name>_pipeline.py
   - # It should fetch data, transform it into a list of Pydantic models, and return them.
3. # Expose an endpoint in app/api/<name>.py that triggers the pipeline and returns the latest data.
4. # Register the router in app/main.py under /api.

Return full file contents for any files you create or change.

