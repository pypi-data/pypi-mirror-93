from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    LOG_LEVEL: str = "debug"
    RELOAD: bool = True
    DEBUG: bool = False
    WORKERS: int = 2
    SENTRY_DSN: str = None


settings = Settings()
