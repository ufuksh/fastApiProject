from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Ogretmen
from pydantic import BaseModel

# Router oluştur
router = APIRouter()

# Pydantic modelleri
class OgretmenBase(BaseModel):
    ad: str
    soyad: str
    brans: str
    iletisim: str

class OgretmenCreate(OgretmenBase):
    pass

class OgretmenResponse(OgretmenBase):
    id: str

    class Config:
        orm_mode = True  # ORM verileriyle çalışmak için gerekli


# CRUD Endpoint'leri

# Öğretmenleri Listele
@router.get("/", response_model=List[OgretmenResponse])
def list_ogretmenler(db: Session = Depends(get_db)):
    """
    Tüm öğretmenleri getir.
    """
    ogretmenler = db.query(Ogretmen).all()
    return ogretmenler


# Öğretmen Detayı
@router.get("/{ogretmen_id}", response_model=OgretmenResponse)
def get_ogretmen(ogretmen_id: str, db: Session = Depends(get_db)):
    """
    Belirli bir öğretmeni ID'ye göre getir.
    """
    ogretmen = db.query(Ogretmen).filter(Ogretmen.id == ogretmen_id).first()
    if not ogretmen:
        raise HTTPException(status_code=404, detail="Öğretmen bulunamadı")
    return ogretmen


# Yeni Öğretmen Ekle
@router.post("/", response_model=OgretmenResponse)
def create_ogretmen(ogretmen: OgretmenCreate, db: Session = Depends(get_db)):
    """
    Yeni bir öğretmen oluştur.
    """
    new_ogretmen = Ogretmen(**ogretmen.dict())
    db.add(new_ogretmen)
    db.commit()
    db.refresh(new_ogretmen)
    return new_ogretmen


# Öğretmen Güncelle
@router.put("/{ogretmen_id}", response_model=OgretmenResponse)
def update_ogretmen(ogretmen_id: str, updated_ogretmen: OgretmenCreate, db: Session = Depends(get_db)):
    """
    Belirli bir öğretmeni güncelle.
    """
    ogretmen = db.query(Ogretmen).filter(Ogretmen.id == ogretmen_id).first()
    if not ogretmen:
        raise HTTPException(status_code=404, detail="Öğretmen bulunamadı")
    
    for key, value in updated_ogretmen.dict().items():
        setattr(ogretmen, key, value)
    
    db.commit()
    db.refresh(ogretmen)
    return ogretmen


# Öğretmen Sil
@router.delete("/{ogretmen_id}")
def delete_ogretmen(ogretmen_id: str, db: Session = Depends(get_db)):
    """
    Belirli bir öğretmeni sil.
    """
    ogretmen = db.query(Ogretmen).filter(Ogretmen.id == ogretmen_id).first()
    if not ogretmen:
        raise HTTPException(status_code=404, detail="Öğretmen bulunamadı")
    
    db.delete(ogretmen)
    db.commit()
    return {"detail": "Öğretmen başarıyla silindi"}
