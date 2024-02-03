
import os
import secrets
from typing import Optional
from pydantic import env_settings



class Settings():
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SQLALCHEMY_URI: str = os.environ.get('SQLALCHEMY_URI') or 'postgresql://gala:pass@localhost:5432/test'
    SENTRY_DSN: Optional[str] = None


def load_config() -> Settings:
    """Load config """
    return Settings()
