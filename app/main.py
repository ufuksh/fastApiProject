# app/main.py

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.routers import ogrenci, ogretmen, ders_programi
from app.database import Base, engine
from app.core.config import settings
from app.core.logger import setup_logger
import uvicorn

# Logger yapılandırmasını çağır
setup_logger()

# FastAPI uygulaması
app = FastAPI(
    title="Ortaöğretim Veri Girişi Sistemi",
    description="Öğrenci, Öğretmen ve Ders Programı Yönetim API'si",
    version="1.0.0"
)

# CORS Ayarları (Gerekliyse)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Üretimde sadece gerekli origin'leri ekleyin
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Statik dosyaları ve şablonları bağla
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Ana sayfa endpoint'i
@app.get("/")
def read_root(request: Request):
    """
    Ana sayfa endpoint'i.
    """
    return templates.TemplateResponse("index.html", {"request": request})

# Uygulama routerlarını dahil et
app.include_router(ogrenci.router, prefix="/ogrenciler", tags=["Öğrenciler"])
app.include_router(ogretmen.router, prefix="/ogretmenler", tags=["Öğretmenler"])
app.include_router(ders_programi.router, prefix="/dersprogrami", tags=["Ders Programı"])

# Uygulama başlatılırken
@app.on_event("startup")
async def startup_event():
    logger.info("Uygulama başlatılıyor...")


# Uygulama kapatılırken
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Uygulama kapatılıyor...")

# Eğer bu dosya doğrudan çalıştırılacaksa
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
