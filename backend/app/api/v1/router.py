from fastapi import APIRouter

from .endpoints import auth, profile, config, session, stats


api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(config.router, prefix="/config", tags=["config"])
api_router.include_router(session.router, prefix="/sessions", tags=["sessions"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
