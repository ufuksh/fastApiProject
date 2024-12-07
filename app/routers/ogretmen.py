# app/routers/ogretmen.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
import logging
from app.schemas import OgretmenCreate, OgretmenRead, OgretmenUpdate
from app.database import get_db
from app.crud import create_ogretmen, get_ogretmenler, update_ogretmen, delete_ogretmen, get_ogretmen_by_id

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

@router.post("/", response_model=OgretmenRead, status_code=status.HTTP_201_CREATED)
def create_ogretmen_endpoint(ogretmen: OgretmenCreate, db: Session = Depends(get_db)):
    """
    Yeni bir öğretmen oluşturur.
    """
    try:
        created_ogretmen = create_ogretmen(db, ogretmen)
        logger.info(f"Yeni öğretmen oluşturuldu: {created_ogretmen.id}")
        return created_ogretmen
    except ValueError as ve:
        logger.error(f"Öğretmen oluşturma hatası: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        logger.exception(f"Öğretmen oluşturma sırasında beklenmeyen hata: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Öğretmen oluşturulurken sunucu hatası oluştu."
        )

@router.get("/", response_model=list[OgretmenRead], status_code=status.HTTP_200_OK)
def list_ogretmenler(db: Session = Depends(get_db)):
    """
    Tüm öğretmenleri listeler.
    """
    try:
        ogretmenler = get_ogretmenler(db)
        logger.info(f"{len(ogretmenler)} öğretmen listelendi.")
        return ogretmenler
    except Exception as e:
        logger.exception(f"Öğretmenler listelenirken beklenmeyen hata: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Öğretmenler listelenirken sunucu hatası oluştu."
        )

@router.get("/{id}", response_model=OgretmenRead, status_code=status.HTTP_200_OK)
def get_ogretmen_endpoint(id: UUID, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip öğretmeni getirir.
    """
    try:
        ogretmen = get_ogretmen_by_id(db, str(id))  # UUID'yi string'e dönüştür
        if not ogretmen:
            logger.warning(f"Öğretmen bulunamadı: {id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Öğretmen bulunamadı."
            )
        return ogretmen
    except HTTPException:
        raise  # HTTPException'ları yeniden yükselt
    except Exception as e:
        logger.exception(f"Öğretmen getirilirken beklenmeyen hata: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Öğretmen getirilirken sunucu hatası oluştu."
        )

@router.put("/{id}", response_model=OgretmenRead, status_code=status.HTTP_200_OK)
def update_ogretmen_endpoint(id: UUID, ogretmen: OgretmenUpdate, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip öğretmeni günceller.
    """
    try:
        updated = update_ogretmen(db, str(id), ogretmen)  # UUID'yi string'e dönüştür
        if not updated:
            logger.warning(f"Güncellenmek istenen öğretmen bulunamadı: {id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Öğretmen bulunamadı."
            )
        logger.info(f"Öğretmen güncellendi: {id}")
        return updated
    except ValueError as ve:
        logger.error(f"Öğretmen güncelleme hatası: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except HTTPException:
        raise  # HTTPException'ları yeniden yükselt
    except Exception as e:
        logger.exception(f"Öğretmen güncellenirken beklenmeyen hata: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Öğretmen güncellenirken sunucu hatası oluştu."
        )

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_ogretmen_endpoint(id: UUID, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip öğretmeni siler.
    """
    try:
        success = delete_ogretmen(db, str(id))  # UUID'yi string'e dönüştür
        if not success:
            logger.warning(f"Öğretmen bulunamadı ve silinemedi: {id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Öğretmen bulunamadı."
            )
        logger.info(f"Öğretmen silindi: {id}")
        return {"detail": f"Öğretmen silindi: {id}"}
    except ValueError as ve:
        logger.error(f"Öğretmen silme hatası: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except HTTPException:
        raise  # HTTPException'ları yeniden yükselt
    except Exception as e:
        logger.exception(f"Öğretmen silinirken beklenmeyen hata: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Öğretmen silinirken sunucu hatası oluştu."
        )
