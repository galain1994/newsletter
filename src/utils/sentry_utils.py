
import sentry_sdk
from ..config import Settings


def sentry_init(settings: Settings):
    """Initial Sentry monitor 初始化Sentry监控"""
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN
        )
