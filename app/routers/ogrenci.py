from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import OgrenciCreate, OgrenciRead, OgrenciUpdate
from app.database import get_db
from app import crud

router = APIRouter()

@router.post("/", response_model=OgrenciRead)
def create_ogrenci(ogrenci: OgrenciCreate, db: Session = Depends(get_db)):
    return crud.create_ogrenci(db, ogrenci)

@router.get("/", response_model=list[OgrenciRead])
def list_ogrenciler(db: Session = Depends(get_db)):
    return crud.get_ogrenciler(db)

@router.put("/{id}", response_model=OgrenciRead)
def update_ogrenci_endpoint(id: UUID, ogrenci: OgrenciUpdate, db: Session = Depends(get_db)):
    updated = crud.update_ogrenci(db, id, ogrenci)
    if not updated:
        raise HTTPException(status_code=404, detail="Öğrenci bulunamadı")
    return updated

@router.delete("/{id}")
def delete_ogrenci_endpoint(id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_ogrenci(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Öğrenci bulunamadı")
    return {"detail": "Öğrenci silindi"}
