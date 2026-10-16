"""
PodiumHQ Configuration Module
Reads configuration from environment variables with strong typing and sensible defaults.
"""

from typing import List, Union
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(default="PodiumHQ", description="Application Name")
    ENVIRONMENT: str = Field(default="development", description="Runtime Environment")
    APP_VERSION: str = Field(default="1.0.0", description="Application Semantic Version")
    LOG_LEVEL: str = Field(default="INFO", description="Logging Verbosity")
    DEBUG: bool = Field(default=False, description="Debug mode")

    # Database Configuration
    DATABASE_URL: str = Field(
        default="sqlite:///./podiumhq.db",
        description="Database Connection URI (PostgreSQL in production, SQLite fallback)",
    )

    # CORS Origins (accepts comma-separated list or JSON array)
    CORS_ORIGINS: Union[str, List[str]] = Field(
        default=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8080", "http://podiumhq.local"],
        description="Allowed CORS origins",
    )

    # Feature Toggles & Prefixes
    RUN_MIGRATIONS: bool = Field(default=False, description="Run DB migrations on startup")
    API_V1_PREFIX: str = Field(default="/api", description="API route prefix")

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return v
        return ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


settings = Settings()
