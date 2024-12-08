from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ogrenciler, ogretmenler, ders_programi
from app.database import Base, engine
import os

# Veritabanını oluştur
Base.metadata.create_all(bind=engine)

# Uygulama oluştur
app = FastAPI(
    title="Ortaöğretim Yönetim Sistemi",
    description="Öğrenci, öğretmen ve ders programı yönetimi için API.",
    version="1.0.0",
)

# CORS Ayarları
origins = [
    "http://localhost",
    "http://localhost:8000",
]  # Geliştirme için izin verilen adresler
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routerları dahil et
app.include_router(ogrenciler.router, prefix="/ogrenciler", tags=["Ogrenciler"])
app.include_router(ogretmenler.router, prefix="/ogretmenler", tags=["Ogretmenler"])
app.include_router(ders_programi.router, prefix="/ders_programi", tags=["Ders Programı"])

# Ana Sayfa
@app.get("/")
def read_root():
    return {"message": "Ortaöğretim Yönetim Sistemi API'ye Hoş Geldiniz!"}
