from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import ogrenci, ogretmen, ders_programi
from app.database import Base, engine
from app.core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(ogrenci.router, prefix="/ogrenciler", tags=["Ogrenciler"])
app.include_router(ogretmen.router, prefix="/ogretmenler", tags=["Ogretmenler"])
app.include_router(ders_programi.router, prefix="/dersprogrami", tags=["Ders Programi"])
