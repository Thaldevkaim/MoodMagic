from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
import os
from typing import List
from pydantic import BaseModel
from datetime import datetime
import json

from config import settings
from ai_generator import AIGenerator
from pinterest_api import fetch_pinterest_images

# Initialize AI Generator
ai_generator = AIGenerator()

# Database setup
engine = create_engine(settings.DATABASE_URL_ASYNC, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database models
class User(Base):
    __tablename__ = "users"
    
    # Define columns with explicit SQLAlchemy types
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    subscription_tier = Column(String(50), default="free")

class Moodboard(Base):
    __tablename__ = "moodboards"
    
    # Define columns with explicit SQLAlchemy types
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String(1000))
    content = Column(JSON)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title="MoodMagic API",
    description="The official API for MoodMagic - Your AI-powered moodboard creation platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MoodboardRequest(BaseModel):
    theme: str
    style: str
    color_palette: List[str]
    mood: str
    additional_notes: str = ""

class MoodboardResponse(BaseModel):
    title: str
    description: str
    content: dict

@app.post("/generate-moodboard", response_model=MoodboardResponse)
async def generate_moodboard(
    request: MoodboardRequest,
    db: Session = Depends(get_db)
):
    try:
        # Generate content using AI
        content = ai_generator.generate_moodboard_content(
            theme=request.theme,
            style=request.style,
            color_palette=request.color_palette,
            mood=request.mood,
            additional_notes=request.additional_notes
        )
        
        # Fetch images from Pinterest
        images = fetch_pinterest_images(
            query=f"{request.theme} {request.style} {request.mood}",
            count=5
        )
        
        # Combine content and images
        moodboard_content = {
            "theme": request.theme,
            "style": request.style,
            "color_palette": request.color_palette,
            "mood": request.mood,
            "content": content,
            "images": images
        }
        
        # Save to database
        moodboard = Moodboard(
            title=f"{request.theme} Moodboard",
            description=content["description"],
            content=moodboard_content
        )
        db.add(moodboard)
        db.commit()
        
        return MoodboardResponse(
            title=moodboard.title,
            description=moodboard.description,
            content=moodboard.content
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/moodboards")
async def get_moodboards(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    moodboards = db.query(Moodboard).offset(skip).limit(limit).all()
    return moodboards

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True if settings.APP_ENV == "development" else False
    ) 