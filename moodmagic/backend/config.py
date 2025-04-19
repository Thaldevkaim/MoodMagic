from pydantic_settings import BaseSettings
from typing import List, Optional
import os
import json

class Settings(BaseSettings):
    # App Info
    APP_NAME: str = "MoodMagic"
    APP_ENV: str = "development"
    BASE_URL: str = "http://localhost:8000"  # Default for development
    
    # Database
    DATABASE_URL: str
    
    # If DATABASE_URL is SQLite, keep it as is. If PostgreSQL, update it for SQLAlchemy
    @property
    def DATABASE_URL_ASYNC(self) -> str:
        if self.DATABASE_URL.startswith("sqlite"):
            return self.DATABASE_URL
        return self.DATABASE_URL.replace("postgres://", "postgresql://")
    
    # API Keys
    OPENAI_API_KEY: str
    SERPAPI_KEY: str
    
    # Security
    JWT_SECRET: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: List[str] | str
    
    @property
    def CORS_ORIGINS_LIST(self) -> List[str]:
        if isinstance(self.CORS_ORIGINS, str):
            try:
                # Try to parse as JSON
                return json.loads(self.CORS_ORIGINS)
            except json.JSONDecodeError:
                # If not JSON, split by comma
                return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
        return self.CORS_ORIGINS
    
    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    
    # Firebase
    FIREBASE_CONFIG: dict = {}
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 