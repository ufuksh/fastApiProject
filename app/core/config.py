# app/core/config.py
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, Field
from typing import List, Optional

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    DEBUG: bool = Field(False, env="DEBUG")
    ALLOWED_ORIGINS: List[AnyHttpUrl] = Field(default_factory=list, env="ALLOWED_ORIGINS")

    class Config:
        env_file = ".env"

settings = Settings()
