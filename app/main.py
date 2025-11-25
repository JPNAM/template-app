from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .core.logging import configure_logging
from .api import health, example  # plus any other routers you add


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

@app.get("/")
def root():
    return {"message": "Template app is running. Try /docs or /api/health."}

app.include_router(health.router, prefix="/api")
app.include_router(example.router, prefix="/api")
app.include_router(pipelines.router, prefix="/api")
