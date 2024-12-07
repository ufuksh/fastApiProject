from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import ogrenci, ogretmen, ders_programi
from app.database import Base, engine
from app.core.config import settings

# Veritabanı tablolarını oluştur
Base.metadata.create_all(bind=engine)

# FastAPI uygulaması
app = FastAPI()

# Statik dosyaları ve şablonları bağla
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Ana sayfa endpoint'i
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Uygulama routerlarını dahil et
app.include_router(ogrenci.router, prefix="/ogrenciler", tags=["Ogrenciler"])
app.include_router(ogretmen.router, prefix="/ogretmenler", tags=["Ogretmenler"])
app.include_router(ders_programi.router, prefix="/dersprogrami", tags=["Ders Programi"])
