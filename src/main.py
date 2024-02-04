

from fastapi import FastAPI, Request, Response
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, scoped_session
from .config import load_config, Settings
from .utils.sentry_utils import sentry_init
from .routers import sub_router


def init_everything(settings: Settings) -> None:
    """Initial Everything to run FastAPI application.
    
    1. Sentry: application monitor
    2. logging
    """
    sentry_init(settings)

    pass


def make_app():
    """Make and initial FastAPI application"""
    app = FastAPI()

    settings = load_config()

    init_everything(settings)

    session_factory = scoped_session(
        sessionmaker(
            bind=create_engine(settings.SQLALCHEMY_URI)
        )
    )
    app.state.session_factory = session_factory

    @app.route('/health')
    async def health_check(request) -> Response:
        return Response(b'success', 200)

    @app.middleware('http')
    async def db_session_middleware(request: Request, call_next) -> Response:
        with session_factory() as db_session:
            request.state.db_session = db_session
            response = await call_next(request)
        return response

    app.include_router(sub_router)

    return app


app = make_app()
