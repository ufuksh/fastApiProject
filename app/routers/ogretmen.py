from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import OgretmenCreate, OgretmenRead, OgretmenUpdate
from app.database import get_db
from app import crud

router = APIRouter()

@router.post("/", response_model=OgretmenRead, status_code=201)
def create_ogretmen(ogretmen: OgretmenCreate, db: Session = Depends(get_db)):
    """
    Yeni bir öğretmen oluşturur.
    """
    try:
        created_ogretmen = crud.create_ogretmen(db, ogretmen)
        return created_ogretmen
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Öğretmen oluşturulurken hata oluştu: {str(e)}"
        )

@router.get("/", response_model=list[OgretmenRead])
def list_ogretmenler(db: Session = Depends(get_db)):
    """
    Tüm öğretmenleri listele.
    """
    try:
        ogretmenler = crud.get_ogretmenler(db)
        return ogretmenler
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Öğretmenler listelenirken hata oluştu: {str(e)}"
        )


@router.put("/{id}", response_model=OgretmenRead)
def update_ogretmen_endpoint(id: UUID, ogretmen: OgretmenUpdate, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip öğretmeni günceller.
    """
    try:
        updated = crud.update_ogretmen(db, id, ogretmen)
        if not updated:
            raise HTTPException(
                status_code=404,
                detail="Öğretmen bulunamadı"
            )
        return updated
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Güncelleme sırasında hata oluştu: {str(e)}"
        )

@router.delete("/{id}", status_code=204)
def delete_ogretmen_endpoint(id: UUID, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip öğretmeni siler.
    """
    try:
        success = crud.delete_ogretmen(db, id)
        if not success:
            raise HTTPException(
                status_code=404,
                detail="Öğretmen bulunamadı"
            )
        return {"detail": "Öğretmen başarıyla silindi"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Silme işlemi sırasında hata oluştu: {str(e)}"
        )
