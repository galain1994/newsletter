
from celery import Celery
from .config import load_config


settings = load_config()

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKDER_URI
)
