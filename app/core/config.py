from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = True

    class Config:
        env_file = ".env"

# Burada settings nesnesi oluşturulmalı
settings = Settings()
