from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager

from .core.config import settings
from .core.database import init_db
from .api.v1.router import api_router
from .api import config, session, profile


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        lifespan=lifespan
    )

    # Session middleware (required for OAuth)
    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.session_secret,
        max_age=600,  # 10 minutes for OAuth state
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(api_router, prefix="/api/v1")
    app.include_router(config.router, prefix="/api/config", tags=["config"])
    app.include_router(session.router, prefix="/api/sessions", tags=["sessions"])
    app.include_router(profile.router, prefix="/api/profile", tags=["profile"])

    @app.get("/")
    async def root():
        return {"message": "Vocab API", "version": settings.VERSION}

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app


app = create_app()
