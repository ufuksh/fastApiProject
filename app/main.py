from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import ogrenci, ogretmen, ders_programi
from app.database import Base, engine
from app.core.config import settings
import logging

# Logger yapılandırması
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Veritabanı tablolarını oluştur
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Veritabanı tabloları başarıyla oluşturuldu.")
except Exception as e:
    logger.error(f"Veritabanı tabloları oluşturulurken hata oluştu: {str(e)}")

# FastAPI uygulaması
app = FastAPI()

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
app.include_router(ogrenci.router, prefix="/ogrenciler", tags=["Ogrenciler"])
app.include_router(ogretmen.router, prefix="/ogretmenler", tags=["Ogretmenler"])
app.include_router(ders_programi.router, prefix="/dersprogrami", tags=["Ders Programi"])

# Uygulama başlatılırken
@app.on_event("startup")
async def startup_event():
    logger.info("Uygulama başlatılıyor...")

# Uygulama kapatılırken
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Uygulama kapatılıyor...")
