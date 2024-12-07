from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import DersProgramiCreate, DersProgramiRead, DersProgramiUpdate
from app.database import get_db
from app import crud

router = APIRouter()

@router.post("/", response_model=DersProgramiRead)
def create_ders_programi(dp: DersProgramiCreate, db: Session = Depends(get_db)):
    return crud.create_ders_programi(db, dp)

@router.get("/", response_model=list[DersProgramiRead])
def list_ders_programlari(db: Session = Depends(get_db)):
    return crud.get_ders_programlari(db)

@router.put("/{id}", response_model=DersProgramiRead)
def update_ders_programi_endpoint(id: UUID, dp: DersProgramiUpdate, db: Session = Depends(get_db)):
    updated = crud.update_ders_programi(db, id, dp)
    if not updated:
        raise HTTPException(status_code=404, detail="Ders programı bulunamadı")
    return updated

@router.delete("/{id}")
def delete_ders_programi_endpoint(id: UUID, db: Session = Depends(get_db)):
    success = crud.delete_ders_programi(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Ders programı bulunamadı")
    return {"detail": "Ders programı silindi"}
