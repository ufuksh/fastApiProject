from sqlalchemy.orm import Session
from uuid import UUID
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
logger.addHandler(handler)


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


def get_ogrenci_by_id(db: Session, id: UUID):
    try:
        ogrenci = db.query(Ogrenci).filter(Ogrenci.id == id).first()
        if ogrenci:
            logger.info(f"Öğrenci bulundu: {id}")
        else:
            logger.warning(f"Öğrenci bulunamadı: {id}")
        return ogrenci
    except Exception as e:
        logger.exception(f"Öğrenci getirilirken hata: {e}")
        raise ValueError(f"Öğrenci getirilirken hata: {e}")


def update_ogrenci(db: Session, id: UUID, ogrenci: OgrenciUpdate):
    try:
        db_ogrenci = get_ogrenci_by_id(db, id)
        if not db_ogrenci:
            logger.warning(f"Güncellenmek istenen öğrenci bulunamadı: {id}")
            return None
        for k, v in ogrenci.dict(exclude_unset=True).items():
            setattr(db_ogrenci, k, v)
        db.commit()
        db.refresh(db_ogrenci)
        logger.info(f"Öğrenci güncellendi: {id}")
        return db_ogrenci
    except Exception as e:
        logger.exception(f"Öğrenci güncellenirken hata: {e}")
        raise ValueError(f"Öğrenci güncellenirken hata: {e}")


def delete_ogrenci(db: Session, id: UUID):
    try:
        logger.info(f"Silinmek istenen öğrenci ID: {id}")
        db_ogrenci = get_ogrenci_by_id(db, id)
        if not db_ogrenci:
            logger.warning(f"Öğrenci bulunamadı: {id}")
            raise ValueError("Öğrenci bulunamadı")
        db.delete(db_ogrenci)
        db.commit()
        logger.info(f"Öğrenci silindi: {id}")
        return db_ogrenci
    except Exception as e:
        logger.exception(f"Silme sırasında hata oluştu: {e}")
        raise ValueError(f"Öğrenci silinirken hata: {e}")


# --- Öğretmen CRUD İşlemleri ---
def get_ogretmen_by_id(db: Session, id: UUID):
    try:
        ogretmen = db.query(Ogretmen).filter(Ogretmen.id == id).first()
        if ogretmen:
            logger.info(f"Öğretmen bulundu: {id}")
        else:
            logger.warning(f"Öğretmen bulunamadı: {id}")
        return ogretmen
    except Exception as e:
        logger.exception(f"Öğretmen getirilirken hata: {e}")
        raise ValueError(f"Öğretmen getirilirken hata: {e}")


def create_ogretmen(db: Session, ogretmen: OgretmenCreate):
    existing_ogretmen = db.query(Ogretmen).filter(Ogretmen.iletisim == ogretmen.iletisim).first()
    if existing_ogretmen:
        logger.error(f"Bu iletişim bilgisi zaten kayıtlı: {ogretmen.iletisim}")
        raise ValueError(f"Bu iletişim bilgisi zaten kayıtlı: {ogretmen.iletisim}")
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


def update_ogretmen(db: Session, id: UUID, ogretmen: OgretmenUpdate):
    try:
        db_ogretmen = get_ogretmen_by_id(db, id)
        if not db_ogretmen:
            logger.warning(f"Güncellenmek istenen öğretmen bulunamadı: {id}")
            return None
        for k, v in ogretmen.dict(exclude_unset=True).items():
            setattr(db_ogretmen, k, v)
        db.commit()
        db.refresh(db_ogretmen)
        logger.info(f"Öğretmen güncellendi: {id}")
        return db_ogretmen
    except Exception as e:
        logger.exception(f"Öğretmen güncellenirken hata: {e}")
        raise ValueError(f"Öğretmen güncellenirken hata: {e}")


def delete_ogretmen(db: Session, id: UUID):
    try:
        logger.info(f"Silinmek istenen öğretmen ID: {id}")
        db_ogretmen = get_ogretmen_by_id(db, id)
        if not db_ogretmen:
            logger.warning(f"Öğretmen bulunamadı: {id}")
            raise ValueError("Öğretmen bulunamadı")
        db.delete(db_ogretmen)
        db.commit()
        logger.info(f"Öğretmen silindi: {id}")
        return db_ogretmen
    except Exception as e:
        logger.exception(f"Öğretmen silinirken hata oluştu: {e}")
        raise ValueError(f"Öğretmen silinirken hata: {e}")


# --- Ders Programı CRUD İşlemleri ---
def get_ders_programi_by_id(db: Session, id: UUID):
    try:
        dp = db.query(DersProgrami).filter(DersProgrami.id == id).first()
        if dp:
            logger.info(f"Ders programı bulundu: {id}")
        else:
            logger.warning(f"Ders programı bulunamadı: {id}")
        return dp
    except Exception as e:
        logger.exception(f"Ders programı getirilirken hata: {e}")
        raise ValueError(f"Ders programı getirilirken hata: {e}")


def create_ders_programi(db: Session, dp: DersProgramiCreate):
    existing_ders_programi = (
        db.query(DersProgrami)
        .filter(
            DersProgrami.sinif == dp.sinif,
            DersProgrami.ders == dp.ders,
            DersProgrami.saat == dp.saat,
        )
        .first()
    )
    if existing_ders_programi:
        logger.error(
            f"Bu ders programı zaten kayıtlı: {dp.sinif}, {dp.ders}, {dp.saat}"
        )
        raise ValueError(
            f"Bu ders programı zaten kayıtlı: {dp.sinif}, {dp.ders}, {dp.saat}"
        )
    try:
        db_dp = DersProgrami(**dp.dict())
        db.add(db_dp)
        db.commit()
        db.refresh(db_dp)
        logger.info(f"Ders programı oluşturuldu: {db_dp.id}")
        return db_dp
    except Exception as e:
        logger.exception(f"Ders programı oluşturulurken hata: {e}")
        raise ValueError(f"Ders programı oluşturulurken hata: {e}")


def get_ders_programlari(db: Session):
    try:
        ders_programlari = db.query(DersProgrami).all()
        logger.info(f"{len(ders_programlari)} ders programı listelendi.")
        return ders_programlari
    except Exception as e:
        logger.exception(f"Ders programları listelenirken hata: {e}")
        raise ValueError(f"Ders programları listelenirken hata: {e}")


def update_ders_programi(db: Session, id: UUID, dp: DersProgramiUpdate):
    try:
        db_dp = get_ders_programi_by_id(db, id)
        if not db_dp:
            logger.warning(f"Güncellenmek istenen ders programı bulunamadı: {id}")
            return None
        for k, v in dp.dict(exclude_unset=True).items():
            setattr(db_dp, k, v)
        db.commit()
        db.refresh(db_dp)
        logger.info(f"Ders programı güncellendi: {id}")
        return db_dp
    except Exception as e:
        logger.exception(f"Ders programı güncellenirken hata: {e}")
        raise ValueError(f"Ders programı güncellenirken hata: {e}")


def delete_ders_programi(db: Session, id: UUID):
    try:
        logger.info(f"Silinmek istenen ders programı ID: {id}")
        db_dp = get_ders_programi_by_id(db, id)
        if not db_dp:
            logger.warning(f"Ders programı bulunamadı: {id}")
            raise ValueError("Ders programı bulunamadı")
        db.delete(db_dp)
        db.commit()
        logger.info(f"Ders programı silindi: {id}")
        return db_dp
    except Exception as e:
        logger.exception(f"Ders programı silinirken hata: {e}")
        raise ValueError(f"Ders programı silinirken hata: {e}")
