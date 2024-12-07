from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import OgrenciCreate, OgrenciRead, OgrenciUpdate
from app.database import get_db
from app.crud import create_ogrenci, get_ogrenciler, update_ogrenci, delete_ogrenci

router = APIRouter()

@router.post("/", response_model=OgrenciRead, status_code=201)
def create_ogrenci_endpoint(ogrenci: OgrenciCreate, db: Session = Depends(get_db)):
    """
    Yeni bir öğrenci oluşturur.
    """
    try:
        created_ogrenci = create_ogrenci(db, ogrenci)
        return created_ogrenci
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Öğrenci oluşturulurken hata oluştu: {str(e)}"
        )

@router.get("/", response_model=list[OgrenciRead])
def list_ogrenciler(db: Session = Depends(get_db)):
    """
    Tüm öğrencileri listele.
    """
    try:
        ogrenciler = get_ogrenciler(db)
        return ogrenciler  # Öğrenciler yoksa boş liste döner.
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Öğrenciler listelenirken hata oluştu: {str(e)}"
        )

@router.put("/{id}", response_model=OgrenciRead)
def update_ogrenci_endpoint(id: UUID, ogrenci: OgrenciUpdate, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip öğrenciyi günceller.
    """
    try:
        updated = update_ogrenci(db, id, ogrenci)
        if not updated:
            raise HTTPException(
                status_code=404,
                detail="Öğrenci bulunamadı"
            )
        return updated
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Güncelleme sırasında hata oluştu: {str(e)}"
        )

def delete_ogrenci(db: Session, id: UUID):
    try:
        print(f"Silinmek istenen öğrenci ID: {id}")
        db_ogrenci = db.query(Ogrenci).filter(Ogrenci.id == id).first()
        if not db_ogrenci:
            print("Öğrenci bulunamadı!")
            return False
        db.delete(db_ogrenci)
        db.commit()
        print("Silme işlemi başarılı!")
        return True
    except Exception as e:
        print(f"Silme sırasında hata oluştu: {e}")
        raise ValueError(f"Öğrenci silinirken hata: {e}")
