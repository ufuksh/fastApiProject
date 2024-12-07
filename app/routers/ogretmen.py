from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import OgretmenCreate, OgretmenRead, OgretmenUpdate
from app.database import get_db
from app import crud

router = APIRouter()

@router.post("/", response_model=OgretmenRead)
def create_ogretmen(ogretmen: OgretmenCreate, db: Session = Depends(get_db)):
    return crud.create_ogretmen(db, ogretmen)

@router.get("/", response_model=list[OgretmenRead])
def list_ogretmenler(db: Session = Depends(get_db)):
    return crud.get_ogretmenler(db)

@router.put("/{id}", response_model=OgretmenRead)
def update_ogretmen_endpoint(id: UUID, ogretmen: OgretmenUpdate, db: Session = Depends(get_db)):
    updated = crud.update_ogretmen(db, id, ogretmen)
    if not updated:
        raise HTTPException(status_code=404, detail="Öğretmen bulunamadı")
    return updated

@router.delete("/{id}")
def delete_ogretmen_endpoint(id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_ogretmen(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Öğretmen bulunamadı")
    return {"detail": "Öğretmen silindi"}
