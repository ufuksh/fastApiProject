from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import DersProgrami, Ogretmen
from pydantic import BaseModel

# Router oluştur
router = APIRouter()

# Pydantic modelleri
class DersProgramiBase(BaseModel):
    sinif: str
    ders: str
    saat: str
    ogretmen_id: str  # İlişkili öğretmen ID'si

class DersProgramiCreate(DersProgramiBase):
    pass

class DersProgramiResponse(DersProgramiBase):
    id: str

    class Config:
        orm_mode = True  # ORM verileriyle çalışmak için gerekli


# CRUD Endpoint'leri

# Ders Programlarını Listele
@router.get("/", response_model=List[DersProgramiResponse])
def list_ders_programi(db: Session = Depends(get_db)):
    """
    Tüm ders programlarını getir.
    """
    ders_programlari = db.query(DersProgrami).all()
    return ders_programlari


# Ders Programı Detayı
@router.get("/{ders_programi_id}", response_model=DersProgramiResponse)
def get_ders_programi(ders_programi_id: str, db: Session = Depends(get_db)):
    """
    Belirli bir ders programını ID'ye göre getir.
    """
    ders_programi = db.query(DersProgrami).filter(DersProgrami.id == ders_programi_id).first()
    if not ders_programi:
        raise HTTPException(status_code=404, detail="Ders programı bulunamadı")
    return ders_programi


# Yeni Ders Programı Ekle
@router.post("/", response_model=DersProgramiResponse)
def create_ders_programi(ders_programi: DersProgramiCreate, db: Session = Depends(get_db)):
    """
    Yeni bir ders programı oluştur.
    """
    # Öğretmen ID'si doğrulama
    ogretmen = db.query(Ogretmen).filter(Ogretmen.id == ders_programi.ogretmen_id).first()
    if not ogretmen:
        raise HTTPException(status_code=400, detail="Geçersiz öğretmen ID")

    new_ders_programi = DersProgrami(**ders_programi.dict())
    db.add(new_ders_programi)
    db.commit()
    db.refresh(new_ders_programi)
    return new_ders_programi


# Ders Programı Güncelle
@router.put("/{ders_programi_id}", response_model=DersProgramiResponse)
def update_ders_programi(
    ders_programi_id: str, updated_ders_programi: DersProgramiCreate, db: Session = Depends(get_db)
):
    """
    Belirli bir ders programını güncelle.
    """
    ders_programi = db.query(DersProgrami).filter(DersProgrami.id == ders_programi_id).first()
    if not ders_programi:
        raise HTTPException(status_code=404, detail="Ders programı bulunamadı")
    
    # Öğretmen ID'si doğrulama
    ogretmen = db.query(Ogretmen).filter(Ogretmen.id == updated_ders_programi.ogretmen_id).first()
    if not ogretmen:
        raise HTTPException(status_code=400, detail="Geçersiz öğretmen ID")

    for key, value in updated_ders_programi.dict().items():
        setattr(ders_programi, key, value)
    
    db.commit()
    db.refresh(ders_programi)
    return ders_programi


# Ders Programı Sil
@router.delete("/{ders_programi_id}")
def delete_ders_programi(ders_programi_id: str, db: Session = Depends(get_db)):
    """
    Belirli bir ders programını sil.
    """
    ders_programi = db.query(DersProgrami).filter(DersProgrami.id == ders_programi_id).first()
    if not ders_programi:
        raise HTTPException(status_code=404, detail="Ders programı bulunamadı")
    
    db.delete(ders_programi)
    db.commit()
    return {"detail": "Ders programı başarıyla silindi"}
