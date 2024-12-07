from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.schemas import DersProgramiCreate, DersProgramiRead, DersProgramiUpdate
from app.database import get_db
from app import crud
import logging

router = APIRouter()

# Logger Ayarları
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(handler)

@router.post("/", response_model=DersProgramiRead, status_code=201)
def create_ders_programi(dp: DersProgramiCreate, db: Session = Depends(get_db)):
    """
    Yeni bir ders programı oluşturur.
    """
    try:
        created_program = crud.create_ders_programi(db, dp)
        logger.info(f"Yeni ders programı oluşturuldu: {created_program.id}")
        return created_program
    except ValueError as ve:
        logger.error(f"Ders programı oluşturma hatası: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.exception(f"Ders programı oluşturulurken beklenmeyen hata: {e}")
        raise HTTPException(status_code=500, detail="Ders programı oluşturulurken sunucu hatası oluştu.")

@router.get("/", response_model=list[DersProgramiRead], status_code=200)
def list_ders_programlari(db: Session = Depends(get_db)):
    """
    Tüm ders programlarını listeler.
    """
    try:
        ders_programlari = crud.get_ders_programlari(db)
        logger.info(f"{len(ders_programlari)} ders programı listelendi.")
        return ders_programlari
    except Exception as e:
        logger.exception(f"Ders programları listelenirken beklenmeyen hata: {e}")
        raise HTTPException(status_code=500, detail="Ders programları listelenirken sunucu hatası oluştu.")

@router.put("/{id}", response_model=DersProgramiRead, status_code=200)
def update_ders_programi_endpoint(id: UUID, dp: DersProgramiUpdate, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip ders programını günceller.
    """
    try:
        updated = crud.update_ders_programi(db, str(id), dp)
        if not updated:
            logger.warning(f"Güncellenmek istenen ders programı bulunamadı: {id}")
            raise HTTPException(status_code=404, detail="Ders programı bulunamadı")
        logger.info(f"Ders programı güncellendi: {id}")
        return updated
    except ValueError as ve:
        logger.error(f"Ders programı güncelleme hatası: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.exception(f"Ders programı güncellenirken beklenmeyen hata: {e}")
        raise HTTPException(status_code=500, detail="Ders programı güncellenirken sunucu hatası oluştu.")

@router.delete("/{id}", status_code=200)
def delete_ders_programi_endpoint(id: UUID, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip ders programını siler.
    """
    try:
        success = crud.delete_ders_programi(db, str(id))
        if not success:
            logger.warning(f"Ders programı silinemedi, bulunamadı: {id}")
            raise HTTPException(status_code=404, detail="Ders programı bulunamadı")
        logger.info(f"Ders programı silindi: {id}")
        return {"detail": "Ders programı başarıyla silindi"}
    except ValueError as ve:
        logger.error(f"Ders programı silme hatası: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.exception(f"Ders programı silinirken beklenmeyen hata: {e}")
        raise HTTPException(status_code=500, detail="Ders programı silinirken sunucu hatası oluştu.")
