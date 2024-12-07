# app/routers/ogretmen.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.schemas import OgretmenCreate, OgretmenRead, OgretmenUpdate
from app.crud import create_ogretmen, get_ogretmenler, get_ogretmen_by_id, update_ogretmen, delete_ogretmen
from app.database import get_db
from app.core.logger import logger  # Global logger'ı import edin

router = APIRouter()

@router.post("/", response_model=OgretmenRead, status_code=status.HTTP_201_CREATED)
def create_ogretmen_endpoint(ogretmen: OgretmenCreate, db: Session = Depends(get_db)):
    try:
        return create_ogretmen(db, ogretmen)
    except ValueError as ve:
        # Kullanıcıya uygun hata mesajı döndür
        logger.error(f"Öğretmen oluşturma hatası: {ve}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        # Beklenmeyen hatalar için genel bir hata mesajı
        logger.error(f"Beklenmeyen hata: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="İç sunucu hatası")

@router.get("/", response_model=List[OgretmenRead])
def read_ogretmenler_endpoint(db: Session = Depends(get_db)):
    try:
        return get_ogretmenler(db)
    except ValueError as ve:
        logger.error(f"Öğretmenler listelenirken hata: {ve}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ve))
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="İç sunucu hatası")

@router.get("/{id}", response_model=OgretmenRead)
def read_ogretmen_endpoint(id: UUID, db: Session = Depends(get_db)):
    try:
        ogretmen = get_ogretmen_by_id(db, str(id))
        if not ogretmen:
            logger.warning(f"Öğretmen bulunamadı: {id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Öğretmen bulunamadı")
        return ogretmen
    except Exception as e:
        logger.error(f"Öğretmen getirilirken hata: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="İç sunucu hatası")

@router.put("/{id}", response_model=OgretmenRead)
def update_ogretmen_endpoint(id: UUID, ogretmen: OgretmenUpdate, db: Session = Depends(get_db)):
    try:
        updated_ogretmen = update_ogretmen(db, str(id), ogretmen)
        if not updated_ogretmen:
            logger.warning(f"Öğretmen bulunamadı ve güncellenemedi: {id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Öğretmen bulunamadı")
        return updated_ogretmen
    except ValueError as ve:
        logger.error(f"Öğretmen güncellenirken hata: {ve}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="İç sunucu hatası")

@router.delete("/{id}", response_model=OgretmenRead)
def delete_ogretmen_endpoint(id: UUID, db: Session = Depends(get_db)):
    try:
        deleted_ogretmen = delete_ogretmen(db, str(id))
        return deleted_ogretmen
    except ValueError as ve:
        logger.error(f"Öğretmen silinirken hata: {ve}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ve))
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="İç sunucu hatası")
