"""
PT Injani Systems - Fullstack Developer Prescreening
Application Configuration and Environment Settings
"""

import os
from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = "Injani Systems Fullstack API"
    environment: str = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))
    port: int = Field(default_factory=lambda: int(os.getenv("PORT", "8000")))

    # Authentication & Security Secrets (loaded from environment)
    # Fail-closed: empty default ensures no predictable fallback secret in application runtime.
    jwt_secret: str = Field(
        default_factory=lambda: os.getenv("JWT_SECRET", "")
    )
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    webhook_secret: str = Field(
        default_factory=lambda: os.getenv("WEBHOOK_SECRET", "")
    )

    # Database
    database_url: str = Field(
        default_factory=lambda: os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:postgres@localhost:5432/injani_db"
        )
    )

    # Local LLM Service
    ollama_url: str = Field(
        default_factory=lambda: os.getenv("OLLAMA_URL", "http://localhost:11434")
    )
    llm_model: str = Field(
        default_factory=lambda: os.getenv("LLM_MODEL", "gemma3:4b")
    )


settings = Settings()
