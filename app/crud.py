from sqlalchemy.orm import Session
from uuid import UUID
from app.models import Ogrenci, Ogretmen, DersProgrami
from app.schemas import (
    OgrenciCreate, OgrenciUpdate,
    OgretmenCreate, OgretmenUpdate,
    DersProgramiCreate, DersProgramiUpdate
)


# Öğrenci CRUD İşlemleri
def create_ogrenci(db: Session, ogrenci: OgrenciCreate):
    # Benzersizlik kontrolü
    existing_ogrenci = db.query(Ogrenci).filter(Ogrenci.ogrenci_numarasi == ogrenci.ogrenci_numarasi).first()
    if existing_ogrenci:
        raise ValueError(f"Bu öğrenci numarası zaten kayıtlı: {ogrenci.ogrenci_numarasi}")
    try:
        db_ogrenci = Ogrenci(**ogrenci.dict())
        db.add(db_ogrenci)
        db.commit()
        db.refresh(db_ogrenci)
        return db_ogrenci
    except Exception as e:
        raise ValueError(f"Öğrenci oluşturulurken hata: {e}")


def get_ogrenciler(db: Session):
    try:
        return db.query(Ogrenci).all()
    except Exception as e:
        raise ValueError(f"Öğrenciler listelenirken hata: {e}")

def get_ogrenci_by_id(db: Session, id: UUID):
    try:
        return db.query(Ogrenci).filter(Ogrenci.id == id).first()
    except Exception as e:
        raise ValueError(f"Öğrenci getirilirken hata: {e}")

def update_ogrenci(db: Session, id: UUID, ogrenci: OgrenciUpdate):
    try:
        db_ogrenci = get_ogrenci_by_id(db, id)
        if not db_ogrenci:
            return None
        for k, v in ogrenci.dict(exclude_unset=True).items():
            setattr(db_ogrenci, k, v)
        db.commit()
        db.refresh(db_ogrenci)
        return db_ogrenci
    except Exception as e:
        raise ValueError(f"Öğrenci güncellenirken hata: {e}")

def delete_ogrenci(db: Session, id: UUID):
    try:
        db_ogrenci = get_ogrenci_by_id(db, id)
        if not db_ogrenci:
            return False
        db.delete(db_ogrenci)
        db.commit()
        return True
    except Exception as e:
        raise ValueError(f"Öğrenci silinirken hata: {e}")


# Öğretmen CRUD İşlemleri
def create_ogretmen(db: Session, ogretmen: OgretmenCreate):
    # Benzersizlik kontrolü
    existing_ogretmen = db.query(Ogretmen).filter(Ogretmen.iletisim == ogretmen.iletisim).first()
    if existing_ogretmen:
        raise ValueError(f"Bu iletişim bilgisi zaten kayıtlı: {ogretmen.iletisim}")
    try:
        db_ogretmen = Ogretmen(**ogretmen.dict())
        db.add(db_ogretmen)
        db.commit()
        db.refresh(db_ogretmen)
        return db_ogretmen
    except Exception as e:
        raise ValueError(f"Öğretmen oluşturulurken hata: {e}")

def get_ogretmenler(db: Session):
    try:
        return db.query(Ogretmen).all()
    except Exception as e:
        raise ValueError(f"Öğretmenler listelenirken hata: {e}")

def update_ogretmen(db: Session, id: UUID, ogretmen: OgretmenUpdate):
    try:
        db_ogretmen = get_ogretmen_by_id(db, id)
        if not db_ogretmen:
            return None
        for k, v in ogretmen.dict(exclude_unset=True).items():
            setattr(db_ogretmen, k, v)
        db.commit()
        db.refresh(db_ogretmen)
        return db_ogretmen
    except Exception as e:
        raise ValueError(f"Öğretmen güncellenirken hata: {e}")

def delete_ogretmen(db: Session, id: UUID):
    try:
        db_ogretmen = get_ogretmen_by_id(db, id)
        if not db_ogretmen:
            return False
        db.delete(db_ogretmen)
        db.commit()
        return True
    except Exception as e:
        raise ValueError(f"Öğretmen silinirken hata: {e}")


# Ders Programı CRUD İşlemleri
def create_ders_programi(db: Session, dp: DersProgramiCreate):
    # Benzersizlik kontrolü
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
        raise ValueError(
            f"Bu ders programı zaten kayıtlı: {dp.sinif}, {dp.ders}, {dp.saat}"
        )
    try:
        db_dp = DersProgrami(**dp.dict())
        db.add(db_dp)
        db.commit()
        db.refresh(db_dp)
        return db_dp
    except Exception as e:
        raise ValueError(f"Ders programı oluşturulurken hata: {e}")

def get_ders_programlari(db: Session):
    try:
        return db.query(DersProgrami).all()
    except Exception as e:
        raise ValueError(f"Ders programları listelenirken hata: {e}")

def update_ders_programi(db: Session, id: UUID, dp: DersProgramiUpdate):
    try:
        db_dp = get_ders_programi_by_id(db, id)
        if not db_dp:
            return None
        for k, v in dp.dict(exclude_unset=True).items():
            setattr(db_dp, k, v)
        db.commit()
        db.refresh(db_dp)
        return db_dp
    except Exception as e:
        raise ValueError(f"Ders programı güncellenirken hata: {e}")

def delete_ders_programi(db: Session, id: UUID):
    try:
        db_dp = get_ders_programi_by_id(db, id)
        if not db_dp:
            return False
        db.delete(db_dp)
        db.commit()
        return True
    except Exception as e:
        raise ValueError(f"Ders programı silinirken hata: {e}")
