import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Template App")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    EXTERNAL_API_BASE_URL: str | None = os.getenv("EXTERNAL_API_BASE_URL")
    EXTERNAL_API_KEY: str | None = os.getenv("EXTERNAL_API_KEY")


settings = Settings()
