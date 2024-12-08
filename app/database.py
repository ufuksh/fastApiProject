from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Veritabanı motorunu oluştur
engine = create_engine(
    settings.DATABASE_URL,  # .env dosyasındaki veritabanı bağlantısı
    pool_pre_ping=True,     # Bağlantı kontrolü
    echo=settings.DEBUG,    # DEBUG modunda SQL sorgularını konsola yazdır
)

# Oturum oluşturucu
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Taban sınıfı (Modeller bu sınıftan türetilir)
Base = declarative_base()

# Veritabanı bağlantısını yöneten bir yardımcı fonksiyon
def get_db():
    """
    Veritabanı oturumu oluşturur ve otomatik olarak kapatır.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
