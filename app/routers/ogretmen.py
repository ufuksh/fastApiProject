from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import OgretmenCreate, OgretmenRead, OgretmenUpdate
from app.database import get_db
from app import crud

router = APIRouter()

@router.post("/", response_model=OgretmenRead)
def create_ogretmen(ogretmen: OgretmenCreate, db: Session = Depends(get_db)):
    """
    Yeni bir öğretmen oluşturur.
    """
    try:
        return crud.create_ogretmen(db, ogretmen)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Öğretmen oluşturulurken hata oluştu: {str(e)}")

@router.get("/", response_model=list[OgretmenRead])
def list_ogretmenler(db: Session = Depends(get_db)):
    """
    Tüm öğretmenleri listele.
    """
    ogretmenler = crud.get_ogretmenler(db)
    if not ogretmenler:
        raise HTTPException(status_code=404, detail="Hiç öğretmen bulunamadı")
    return ogretmenler

@router.put("/{id}", response_model=OgretmenRead)
def update_ogretmen_endpoint(id: UUID, ogretmen: OgretmenUpdate, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip öğretmeni günceller.
    """
    try:
        updated = crud.update_ogretmen(db, id, ogretmen)
        if not updated:
            raise HTTPException(status_code=404, detail="Öğretmen bulunamadı")
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Güncelleme sırasında hata oluştu: {str(e)}")

@router.delete("/{id}")
def delete_ogretmen_endpoint(id: UUID, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip öğretmeni siler.
    """
    try:
        success = crud.delete_ogretmen(db, id)
        if not success:
            raise HTTPException(status_code=404, detail="Öğretmen bulunamadı")
        return {"detail": "Öğretmen başarıyla silindi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Silme işlemi sırasında hata oluştu: {str(e)}")
