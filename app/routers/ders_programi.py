from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import DersProgramiCreate, DersProgramiRead, DersProgramiUpdate
from app.database import get_db
from app import crud

router = APIRouter()

@router.post("/", response_model=DersProgramiRead)
def create_ders_programi(dp: DersProgramiCreate, db: Session = Depends(get_db)):
    """
    Yeni bir ders programı oluşturur.
    """
    try:
        return crud.create_ders_programi(db, dp)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ders programı oluşturulurken hata oluştu: {str(e)}")

@router.get("/", response_model=list[DersProgramiRead])
def list_ders_programlari(db: Session = Depends(get_db)):
    """
    Tüm ders programlarını listele.
    """
    ders_programlari = crud.get_ders_programlari(db)
    if not ders_programlari:
        raise HTTPException(status_code=404, detail="Hiç ders programı bulunamadı")
    return ders_programlari

@router.put("/{id}", response_model=DersProgramiRead)
def update_ders_programi_endpoint(id: UUID, dp: DersProgramiUpdate, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip ders programını günceller.
    """
    try:
        updated = crud.update_ders_programi(db, id, dp)
        if not updated:
            raise HTTPException(status_code=404, detail="Ders programı bulunamadı")
        return updated
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Güncelleme sırasında hata oluştu: {str(e)}")

@router.delete("/{id}")
def delete_ders_programi_endpoint(id: UUID, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip ders programını siler.
    """
    try:
        success = crud.delete_ders_programi(db, id)
        if not success:
            raise HTTPException(status_code=404, detail="Ders programı bulunamadı")
        return {"detail": "Ders programı başarıyla silindi"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Silme işlemi sırasında hata oluştu: {str(e)}")
