# app/routers/ogrenci.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
import logging
from app.schemas import OgrenciCreate, OgrenciRead, OgrenciUpdate
from app.database import get_db
from app.crud import create_ogrenci, get_ogrenciler, get_ogrenci_by_id, update_ogrenci, delete_ogrenci

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

@router.post("/", response_model=OgrenciRead, status_code=status.HTTP_201_CREATED)
def create_ogrenci_endpoint(ogrenci: OgrenciCreate, db: Session = Depends(get_db)):
    """
    Yeni bir öğrenci oluşturur.
    """
    try:
        created_ogrenci = create_ogrenci(db, ogrenci)
        logger.info(f"Yeni öğrenci oluşturuldu: {created_ogrenci.id}")
        return created_ogrenci
    except ValueError as ve:
        logger.error(f"Öğrenci oluşturma hatası: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        logger.exception(f"Öğrenci oluşturma sırasında beklenmeyen hata: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Öğrenci oluşturulurken sunucu hatası oluştu."
        )

@router.get("/", response_model=list[OgrenciRead], status_code=status.HTTP_200_OK)
def list_ogrenciler(db: Session = Depends(get_db)):
    """
    Tüm öğrencileri listeler.
    """
    try:
        ogrenciler = get_ogrenciler(db)
        logger.info(f"{len(ogrenciler)} öğrenci listelendi.")
        return ogrenciler
    except Exception as e:
        logger.exception(f"Öğrenciler listelenirken beklenmeyen hata: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Öğrenciler listelenirken sunucu hatası oluştu."
        )

@router.get("/{id}", response_model=OgrenciRead, status_code=status.HTTP_200_OK)
def get_ogrenci_endpoint(id: UUID, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip öğrenciyi getirir.
    """
    try:
        ogrenci = get_ogrenci_by_id(db, str(id))  # UUID'yi string'e dönüştür
        if not ogrenci:
            logger.warning(f"Öğrenci bulunamadı: {id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Öğrenci bulunamadı."
            )
        return ogrenci
    except HTTPException:
        raise  # HTTPException'ları yeniden yükselt
    except Exception as e:
        logger.exception(f"Öğrenci getirilirken beklenmeyen hata: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Öğrenci getirilirken sunucu hatası oluştu."
        )

@router.put("/{id}", response_model=OgrenciRead, status_code=status.HTTP_200_OK)
def update_ogrenci_endpoint(id: UUID, ogrenci: OgrenciUpdate, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip öğrenciyi günceller.
    """
    try:
        updated = update_ogrenci(db, str(id), ogrenci)  # UUID'yi string'e dönüştür
        if not updated:
            logger.warning(f"Güncellenmek istenen öğrenci bulunamadı: {id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Öğrenci bulunamadı."
            )
        logger.info(f"Öğrenci güncellendi: {id}")
        return updated
    except ValueError as ve:
        logger.error(f"Öğrenci güncelleme hatası: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except HTTPException:
        raise  # HTTPException'ları yeniden yükselt
    except Exception as e:
        logger.exception(f"Öğrenci güncellenirken beklenmeyen hata: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Öğrenci güncellenirken sunucu hatası oluştu."
        )

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_ogrenci_endpoint(id: UUID, db: Session = Depends(get_db)):
    """
    Belirtilen ID'ye sahip öğrenciyi siler.
    """
    try:
        success = delete_ogrenci(db, str(id))  # UUID'yi string'e dönüştür
        if not success:
            logger.warning(f"Öğrenci bulunamadı ve silinemedi: {id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Öğrenci bulunamadı."
            )
        logger.info(f"Öğrenci silindi: {id}")
        return {"detail": f"Öğrenci silindi: {id}"}
    except ValueError as ve:
        logger.error(f"Öğrenci silme hatası: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except HTTPException:
        raise  # HTTPException'ları yeniden yükselt
    except Exception as e:
        logger.exception(f"Öğrenci silinirken beklenmeyen hata: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Öğrenci silinirken sunucu hatası oluştu."
        )
