from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # App Info
    APP_NAME: str = "MoodMagic"
    APP_ENV: str = "development"
    BASE_URL: str = "http://localhost:8000"  # Default for development
    
    # API Keys
    OPENAI_API_KEY: str
    SERPAPI_KEY: str
    
    # Database
    DATABASE_URL: str = "sqlite:///./moodmagic.db"  # Default to SQLite for development
    
    # Security
    JWT_SECRET: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: List[str] = ["https://moodmagic.app", "http://localhost:3000"]
    
    # Stripe
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    
    # Firebase
    FIREBASE_CONFIG: dict = {}
    
    class Config:
        env_file = ".env"

settings = Settings() 