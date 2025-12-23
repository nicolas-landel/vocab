from pydantic_settings import BaseSettings
from typing import List
import json
import os


class Settings(BaseSettings):
    PROJECT_NAME: str = "Vocab API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"  # development, staging, production
    
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # CORS - can be set as JSON string in env or use default
    CORS_ORIGINS: str = '["http://localhost:5173", "http://localhost:5174", "http://localhost:8080"]'
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse CORS_ORIGINS from JSON string to list"""
        if isinstance(self.CORS_ORIGINS, str):
            return json.loads(self.CORS_ORIGINS)
        return self.CORS_ORIGINS
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Session (for OAuth state)
    SESSION_SECRET: str = ""  # Will default to SECRET_KEY if not set
    
    @property
    def session_secret(self) -> str:
        """Use SESSION_SECRET if set, otherwise fall back to SECRET_KEY"""
        return self.SESSION_SECRET if self.SESSION_SECRET else self.SECRET_KEY
    
    # Google OAuth
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
