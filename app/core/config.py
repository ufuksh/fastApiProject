from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Uygulama ayarları
    APP_NAME: str = "Ortaöğretim Veri Yönetimi Sistemi"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Veritabanı bağlantı bilgileri
    DATABASE_URL: str  # .env'de belirtilmelidir (ör. mysql+pymysql://user:password@localhost:3306/dbname)


    # JWT veya başka güvenlik sistemleri için
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Token süresi (dakika)
    ALGORITHM: str = "HS256"  # Şifreleme algoritması

    class Config:
        env_file = ".env"  # Çevresel değişkenleri .env dosyasından alır
        env_file_encoding = "utf-8"  # .env dosyası için karakter kodlaması


# Global settings nesnesi
settings = Settings()
