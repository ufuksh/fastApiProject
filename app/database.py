# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings
from sqlalchemy.exc import SQLAlchemyError
import logging

# Logger Ayarları
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)

# Veritabanı bağlantı motoru
try:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_size=20,          # Bağlantı havuzu boyutu
        max_overflow=0,        # Ek bağlantı sayısı
        pool_timeout=30,       # Bağlantı havuzundan bağlantı almak için maksimum süre (saniye)
        pool_recycle=1800      # Bağlantıların yeniden kullanılması için süre (saniye)
    )
    logger.info("Veritabanı bağlantısı başarıyla oluşturuldu.")
except SQLAlchemyError as e:
    logger.exception(f"Veritabanı bağlantısı oluşturulurken hata oluştu: {e}")
    raise

# Oturum yönetimi için sessionmaker
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Model tabanını tanımlama
Base = declarative_base()

# Veritabanı oturumu için bir bağlam yöneticisi
def get_db() -> Session:
    """
    Veritabanı oturumu sağlayıcısı.
    Bu fonksiyon, FastAPI bağımlılıkları tarafından kullanılacak ve her istek için yeni bir oturum sağlayacaktır.
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.exception(f"Veritabanı işlemi sırasında hata oluştu: {e}")
        db.rollback()
        raise RuntimeError(f"Veritabanı işlemi sırasında hata oluştu: {str(e)}")
    finally:
        db.close()
        logger.info("Veritabanı oturumu kapatıldı.")
