"""
Project Abhaya — Centralized Configuration
Loads settings from .env using pydantic-settings.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables / .env file."""

    # --- Google Gemini AI ---
    gemini_api_key: str = "your_gemini_api_key_here"

    # --- MongoDB ---
    mongo_uri: str = "mongodb://localhost:27017"
    mongo_db_name: str = "abhaya_database"

    # --- CORS ---
    cors_origins: str = "*"

    # --- App Metadata ---
    app_title: str = "Project Abhaya AI/ML Engine"
    app_description: str = "Microservice providing predictive health and generative wellness capabilities."
    app_version: str = "1.0.0"

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton — loaded once, reused everywhere."""
    return Settings()
