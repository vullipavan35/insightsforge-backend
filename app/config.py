import os
from enum import Enum
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    # Core Environment
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    PROJECT_NAME: str = "InsightForge AI Lite Monolith"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql://localhost:5432/insightsforge_dev"
    DB_ECHO: bool = False

    # Redis Cache
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security & JWT
    SECRET_KEY: str = "dev-secret-key-for-insightsforge-local-monolith"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # File Storage
    FILE_UPLOAD_DIR: str = "./uploads/dev"
    MAX_FILE_SIZE_MB: int = 500

    # API Documentation & Rate Limiting
    ENABLE_API_DOCS: bool = True
    RATE_LIMIT_REQUESTS: int = 1000
    RATE_LIMIT_WINDOW_SECONDS: int = 60

    model_config = SettingsConfigDict(
        env_file=(
            f".env.{os.getenv('ENVIRONMENT', 'development')}",
            ".env.development",
            ".env",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
