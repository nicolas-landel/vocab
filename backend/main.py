"""
Entry point for running the FastAPI application.
This file exists at the root level for compatibility with deployment tools.
The actual app is defined in app/main.py following FastAPI best practices.
"""
from app.main import app

__all__ = ["app"]
