from fastapi import FastAPI
from app.routers import ogrenciler, ogretmenler, ders_programi
from app.database import engine
from app.models import Base

# Veritabanı tablolarını oluştur (Eğer Alembic kullanılmıyorsa)
Base.metadata.create_all(bind=engine)

# FastAPI uygulamasını başlat
app = FastAPI(
    title="Ortaöğretim Veri Yönetimi Sistemi",
    description="Öğrenci, öğretmen ve ders programlarını yöneten bir API.",
    version="1.0.0",
)

# Router'ları bağla
app.include_router(ogrenciler.router, prefix="/ogrenciler", tags=["Öğrenciler"])
app.include_router(ogretmenler.router, prefix="/ogretmenler", tags=["Öğretmenler"])
app.include_router(ders_programi.router, prefix="/ders_programi", tags=["Ders Programı"])
