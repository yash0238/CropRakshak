"""
Configuration management for Krishivaani Backend
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Krishivaani"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # API Keys
    GOOGLE_API_KEY: str
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # BigQuery
    BIGQUERY_PROJECT_ID: str
    BIGQUERY_DATASET_ID: str = "krisisar_analytics"
    BIGQUERY_CREDENTIALS_PATH: Optional[str] = None
    # Table that holds the bulk farm-performance dataset (the 500K synthetic
    # rows, or real data.gov.in rows). Loaded via CSV auto-detect, so `location`
    # is a STRING containing JSON — the queries use JSON_EXTRACT_SCALAR which
    # works on STRING columns too. Override in .env if you named it differently.
    BIGQUERY_FARM_TABLE: str = "farm_perf_raw"
    
    # External APIs
    OPEN_METEO_API_URL: str = "https://api.open-meteo.com/v1/forecast"
    NASA_POWER_API_URL: Optional[str] = None
    AGMARKNET_API_URL: Optional[str] = None

    # Sarvam AI (India-first multilingual LLM — used for the chat assistant &
    # farmer-facing text so Indian-language answers are more natural than Gemini.
    # If SARVAM_API_KEY is unset, the code automatically falls back to Gemini,
    # so the app keeps working without it.)
    SARVAM_API_KEY: Optional[str] = None
    SARVAM_API_URL: str = "https://api.sarvam.ai/v1/chat/completions"
    # sarvam-m was deprecated; use sarvam-30b (fast, good for chat) or
    # sarvam-105b (higher quality, slower). Override via SARVAM_MODEL in .env.
    SARVAM_MODEL: str = "sarvam-30b"
    
    # Gemini Configuration (GA model names — avoid -exp aliases that get retired)
    # NOTE: gemini-2.5-pro has 0 quota on the free tier, so we use flash for the
    # "pro" slot too. Switch GEMINI_MODEL_PRO back to gemini-2.5-pro once on a
    # paid/billing-enabled key for higher-quality reasoning.
    GEMINI_MODEL_FLASH: str = "gemini-2.5-flash"
    GEMINI_MODEL_PRO: str = "gemini-2.5-flash"
    GEMINI_MODEL_VISION: str = "gemini-2.5-flash"
    GEMINI_TEMPERATURE: float = 0.7
    GEMINI_MAX_TOKENS: int = 8192
    
    # ChromaDB (for RAG)
    CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_TYPES: list = ["image/jpeg", "image/png", "image/jpg"]
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Firebase Storage (optional)
    FIREBASE_API_KEY: Optional[str] = None
    FIREBASE_AUTH_DOMAIN: Optional[str] = None
    FIREBASE_PROJECT_ID: Optional[str] = None
    FIREBASE_STORAGE_BUCKET: Optional[str] = None
    FIREBASE_MESSAGING_SENDER_ID: Optional[str] = None
    FIREBASE_APP_ID: Optional[str] = None
    
    # Auth (optional, matches .env.example naming)
    AUTH_SECRET: Optional[str] = None
    AUTH_URL: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # tolerate future/optional keys in .env without crashing

# Initialize settings
settings = Settings()

# Validate critical settings
if not settings.GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is required")

if not settings.DATABASE_URL:
    raise ValueError("DATABASE_URL is required")

if not settings.BIGQUERY_PROJECT_ID:
    raise ValueError("BIGQUERY_PROJECT_ID is required")
