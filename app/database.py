from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from sqlalchemy.exc import SQLAlchemyError

# Veritabanı bağlantı motoru
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)

# Oturum yönetimi için sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Model tabanını tanımlama
Base = declarative_base()

# Veritabanı oturumu için bir bağlam yöneticisi
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Veritabanı işlemi sırasında hata oluştu: {str(e)}")
    finally:
        db.close()
