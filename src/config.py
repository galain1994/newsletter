
import os
import secrets
from typing import Optional



class Settings():
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SQLALCHEMY_URI: str = os.environ.get('SQLALCHEMY_URI') or 'postgresql://gala:pass@localhost:5432/test'
    CELERY_BROKDER_URI: str = os.environ.get('CELERY_BROKDER_URI') or ''
    SENTRY_DSN: Optional[str] = None


def load_config() -> Settings:
    """Load config """
    return Settings()
