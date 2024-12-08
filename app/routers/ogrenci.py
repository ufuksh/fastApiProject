from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Ogrenci
from pydantic import BaseModel

# Router oluştur
router = APIRouter()

# Pydantic modelleri
class OgrenciBase(BaseModel):
    ad: str
    soyad: str
    ogrenci_numarasi: str
    sinif: str
    iletisim: str

class OgrenciCreate(OgrenciBase):
    pass

class OgrenciResponse(OgrenciBase):
    id: str

    class Config:
        orm_mode = True  # ORM verileriyle çalışmak için gerekli


# CRUD Endpoint'leri

# Öğrencileri Listele
@router.get("/", response_model=List[OgrenciResponse])
def list_ogrenciler(db: Session = Depends(get_db)):
    """
    Tüm öğrencileri getir.
    """
    ogrenciler = db.query(Ogrenci).all()
    return ogrenciler


# Öğrenci Detayı
@router.get("/{ogrenci_id}", response_model=OgrenciResponse)
def get_ogrenci(ogrenci_id: str, db: Session = Depends(get_db)):
    """
    Belirli bir öğrenciyi ID'ye göre getir.
    """
    ogrenci = db.query(Ogrenci).filter(Ogrenci.id == ogrenci_id).first()
    if not ogrenci:
        raise HTTPException(status_code=404, detail="Öğrenci bulunamadı")
    return ogrenci


# Yeni Öğrenci Ekle
@router.post("/", response_model=OgrenciResponse)
def create_ogrenci(ogrenci: OgrenciCreate, db: Session = Depends(get_db)):
    """
    Yeni bir öğrenci oluştur.
    """
    new_ogrenci = Ogrenci(**ogrenci.dict())
    db.add(new_ogrenci)
    db.commit()
    db.refresh(new_ogrenci)
    return new_ogrenci


# Öğrenci Güncelle
@router.put("/{ogrenci_id}", response_model=OgrenciResponse)
def update_ogrenci(ogrenci_id: str, updated_ogrenci: OgrenciCreate, db: Session = Depends(get_db)):
    """
    Belirli bir öğrenciyi güncelle.
    """
    ogrenci = db.query(Ogrenci).filter(Ogrenci.id == ogrenci_id).first()
    if not ogrenci:
        raise HTTPException(status_code=404, detail="Öğrenci bulunamadı")
    
    for key, value in updated_ogrenci.dict().items():
        setattr(ogrenci, key, value)
    
    db.commit()
    db.refresh(ogrenci)
    return ogrenci


# Öğrenci Sil
@router.delete("/{ogrenci_id}")
def delete_ogrenci(ogrenci_id: str, db: Session = Depends(get_db)):
    """
    Belirli bir öğrenciyi sil.
    """
    ogrenci = db.query(Ogrenci).filter(Ogrenci.id == ogrenci_id).first()
    if not ogrenci:
        raise HTTPException(status_code=404, detail="Öğrenci bulunamadı")
    
    db.delete(ogrenci)
    db.commit()
    return {"detail": "Öğrenci başarıyla silindi"}
