# app/crud.py

from sqlalchemy.orm import Session
import logging
from app.models import Ogrenci, Ogretmen, DersProgrami
from app.schemas import (
    OgrenciCreate, OgrenciUpdate,
    OgretmenCreate, OgretmenUpdate,
    DersProgramiCreate, DersProgramiUpdate
)

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

# --- Genel CRUD Yardımcı Fonksiyonları ---

def get_by_id(db: Session, model, id: str):
    """
    Belirtilen model ve ID'ye göre bir nesne getirir.
    """
    try:
        obj = db.query(model).filter(model.id == id).first()
        if obj:
            logger.info(f"{model.__name__} bulundu: {id}")
        else:
            logger.warning(f"{model.__name__} bulunamadı: {id}")
        return obj
    except Exception as e:
        logger.exception(f"{model.__name__} getirilirken hata: {e}")
        raise ValueError(f"{model.__name__} getirilirken hata: {e}")

def delete_by_id(db: Session, model, id: str):
    """
    Belirtilen model ve ID'ye göre bir nesneyi siler.
    """
    try:
        obj = get_by_id(db, model, id)
        if not obj:
            logger.warning(f"{model.__name__} bulunamadı ve silinemedi: {id}")
            raise ValueError(f"{model.__name__} bulunamadı")
        db.delete(obj)
        db.commit()
        logger.info(f"{model.__name__} silindi: {id}")
        return obj
    except Exception as e:
        logger.exception(f"{model.__name__} silinirken hata: {e}")
        raise ValueError(f"{model.__name__} silinirken hata: {e}")

# --- Öğrenci CRUD İşlemleri ---

def create_ogrenci(db: Session, ogrenci: OgrenciCreate):
    existing_ogrenci = db.query(Ogrenci).filter(Ogrenci.ogrenci_numarasi == ogrenci.ogrenci_numarasi).first()
    if existing_ogrenci:
        logger.error(f"Bu öğrenci numarası zaten kayıtlı: {ogrenci.ogrenci_numarasi}")
        raise ValueError(f"Bu öğrenci numarası zaten kayıtlı: {ogrenci.ogrenci_numarasi}")
    try:
        db_ogrenci = Ogrenci(**ogrenci.dict())
        db.add(db_ogrenci)
        db.commit()
        db.refresh(db_ogrenci)
        logger.info(f"Öğrenci oluşturuldu: {db_ogrenci.id}")
        return db_ogrenci
    except Exception as e:
        logger.exception(f"Öğrenci oluşturulurken hata: {e}")
        raise ValueError(f"Öğrenci oluşturulurken hata: {e}")

def get_ogrenciler(db: Session):
    try:
        ogrenciler = db.query(Ogrenci).all()
        logger.info(f"{len(ogrenciler)} öğrenci listelendi.")
        return ogrenciler
    except Exception as e:
        logger.exception(f"Öğrenciler listelenirken hata: {e}")
        raise ValueError(f"Öğrenciler listelenirken hata: {e}")

def get_ogrenci_by_id(db: Session, id: str):
    """
    Belirtilen ID'ye sahip öğrenci kaydını getirir.
    """
    try:
        ogrenci = get_by_id(db, Ogrenci, id)
        return ogrenci
    except Exception as e:
        logger.exception(f"Ogrenci getirilirken hata: {e}")
        raise e

def update_ogrenci(db: Session, id: str, ogrenci: OgrenciUpdate):
    try:
        db_ogrenci = get_ogrenci_by_id(db, id)
        if not db_ogrenci:
            logger.warning(f"Güncellenmek istenen öğrenci bulunamadı: {id}")
            return None
        for key, value in ogrenci.dict(exclude_unset=True).items():
            setattr(db_ogrenci, key, value)
        db.commit()
        db.refresh(db_ogrenci)
        logger.info(f"Öğrenci güncellendi: {id}")
        return db_ogrenci
    except Exception as e:
        logger.exception(f"Öğrenci güncellenirken hata: {e}")
        raise ValueError(f"Öğrenci güncellenirken hata: {e}")

def delete_ogrenci(db: Session, id: str):
    return delete_by_id(db, Ogrenci, id)

# --- Öğretmen CRUD İşlemleri ---

def create_ogretmen(db: Session, ogretmen: OgretmenCreate):
    existing_ogretmen = db.query(Ogretmen).filter(Ogretmen.ogretmen_numarasi == ogretmen.ogretmen_numarasi).first()
    if existing_ogretmen:
        logger.error(f"Bu öğretmen numarası zaten kayıtlı: {ogretmen.ogretmen_numarasi}")
        raise ValueError(f"Bu öğretmen numarası zaten kayıtlı: {ogretmen.ogretmen_numarasi}")
    try:
        db_ogretmen = Ogretmen(**ogretmen.dict())
        db.add(db_ogretmen)
        db.commit()
        db.refresh(db_ogretmen)
        logger.info(f"Öğretmen oluşturuldu: {db_ogretmen.id}")
        return db_ogretmen
    except Exception as e:
        logger.exception(f"Öğretmen oluşturulurken hata: {e}")
        raise ValueError(f"Öğretmen oluşturulurken hata: {e}")

def get_ogretmenler(db: Session):
    try:
        ogretmenler = db.query(Ogretmen).all()
        logger.info(f"{len(ogretmenler)} öğretmen listelendi.")
        return ogretmenler
    except Exception as e:
        logger.exception(f"Öğretmenler listelenirken hata: {e}")
        raise ValueError(f"Öğretmenler listelenirken hata: {e}")

def get_ogretmen_by_id(db: Session, id: str):
    """
    Belirtilen ID'ye sahip öğretmen kaydını getirir.
    """
    try:
        ogretmen = get_by_id(db, Ogretmen, id)
        return ogretmen
    except Exception as e:
        logger.exception(f"Ogretmen getirilirken hata: {e}")
        raise e

def update_ogretmen(db: Session, id: str, ogretmen: OgretmenUpdate):
    try:
        db_ogretmen = get_ogretmen_by_id(db, id)
        if not db_ogretmen:
            logger.warning(f"Güncellenmek istenen öğretmen bulunamadı: {id}")
            return None
        for key, value in ogretmen.dict(exclude_unset=True).items():
            setattr(db_ogretmen, key, value)
        db.commit()
        db.refresh(db_ogretmen)
        logger.info(f"Öğretmen güncellendi: {id}")
        return db_ogretmen
    except Exception as e:
        logger.exception(f"Öğretmen güncellenirken hata: {e}")
        raise ValueError(f"Öğretmen güncellenirken hata: {e}")

def delete_ogretmen(db: Session, id: str):
    return delete_by_id(db, Ogretmen, id)

# --- Ders Programı CRUD İşlemleri ---

def create_ders_programi(db: Session, ders_programi: DersProgramiCreate):
    try:
        db_ders_programi = DersProgrami(**ders_programi.dict())
        db.add(db_ders_programi)
        db.commit()
        db.refresh(db_ders_programi)
        logger.info(f"Ders programı oluşturuldu: {db_ders_programi.id}")
        return db_ders_programi
    except Exception as e:
        logger.exception(f"Ders programı oluşturulurken hata: {e}")
        raise ValueError(f"Ders programı oluşturulurken hata: {e}")

def get_ders_programi(db: Session):
    try:
        ders_programlari = db.query(DersProgrami).all()
        logger.info(f"{len(ders_programlari)} ders programı listelendi.")
        return ders_programlari
    except Exception as e:
        logger.exception(f"Ders programları listelenirken hata: {e}")
        raise ValueError(f"Ders programları listelenirken hata: {e}")

def get_ders_programi_by_id(db: Session, id: str):
    """
    Belirtilen ID'ye sahip ders programı kaydını getirir.
    """
    try:
        ders_programi = get_by_id(db, DersProgrami, id)
        return ders_programi
    except Exception as e:
        logger.exception(f"Ders programı getirilirken hata: {e}")
        raise e

def update_ders_programi(db: Session, id: str, ders_programi: DersProgramiUpdate):
    try:
        db_ders_programi = get_ders_programi_by_id(db, id)
        if not db_ders_programi:
            logger.warning(f"Güncellenmek istenen ders programı bulunamadı: {id}")
            return None
        for key, value in ders_programi.dict(exclude_unset=True).items():
            setattr(db_ders_programi, key, value)
        db.commit()
        db.refresh(db_ders_programi)
        logger.info(f"Ders programı güncellendi: {id}")
        return db_ders_programi
    except Exception as e:
        logger.exception(f"Ders programı güncellenirken hata: {e}")
        raise ValueError(f"Ders programı güncellenirken hata: {e}")

def delete_ders_programi(db: Session, id: str):
    return delete_by_id(db, DersProgrami, id)
