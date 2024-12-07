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
    try:
        db_ogrenci = Ogrenci(**ogrenci.dict())
        db.add(db_ogrenci)
        db.commit()
        db.refresh(db_ogrenci)
        return db_ogrenci
    except Exception as e:
        raise ValueError(f"Öğrenci oluşturulurken hata oluştu: {str(e)}")

def get_ogrenciler(db: Session):
    try:
        return db.query(Ogrenci).all()
    except Exception as e:
        raise ValueError(f"Öğrenciler listelenirken hata oluştu: {str(e)}")

def get_ogrenci_by_id(db: Session, id: UUID):
    try:
        return db.query(Ogrenci).filter(Ogrenci.id == str(id)).first()
    except Exception as e:
        raise ValueError(f"Öğrenci getirilirken hata oluştu: {str(e)}")

def update_ogrenci(db: Session, id: UUID, ogrenci: OgrenciUpdate):
    db_ogrenci = get_ogrenci_by_id(db, id)
    if not db_ogrenci:
        return None
    try:
        for k, v in ogrenci.dict(exclude_unset=True).items():
            setattr(db_ogrenci, k, v)
        db.commit()
        db.refresh(db_ogrenci)
        return db_ogrenci
    except Exception as e:
        raise ValueError(f"Öğrenci güncellenirken hata oluştu: {str(e)}")

def delete_ogrenci(db: Session, id: UUID):
    db_ogrenci = get_ogrenci_by_id(db, id)
    if not db_ogrenci:
        return False
    try:
        db.delete(db_ogrenci)
        db.commit()
        return True
    except Exception as e:
        raise ValueError(f"Öğrenci silinirken hata oluştu: {str(e)}")

# Öğretmen CRUD İşlemleri
def create_ogretmen(db: Session, ogretmen: OgretmenCreate):
    try:
        db_ogretmen = Ogretmen(**ogretmen.dict())
        db.add(db_ogretmen)
        db.commit()
        db.refresh(db_ogretmen)
        return db_ogretmen
    except Exception as e:
        raise ValueError(f"Öğretmen oluşturulurken hata oluştu: {str(e)}")

def get_ogretmenler(db: Session):
    try:
        return db.query(Ogretmen).all()
    except Exception as e:
        raise ValueError(f"Öğretmenler listelenirken hata oluştu: {str(e)}")

def get_ogretmen_by_id(db: Session, id: UUID):
    try:
        return db.query(Ogretmen).filter(Ogretmen.id == str(id)).first()
    except Exception as e:
        raise ValueError(f"Öğretmen getirilirken hata oluştu: {str(e)}")

def update_ogretmen(db: Session, id: UUID, ogretmen: OgretmenUpdate):
    db_ogretmen = get_ogretmen_by_id(db, id)
    if not db_ogretmen:
        return None
    try:
        for k, v in ogretmen.dict(exclude_unset=True).items():
            setattr(db_ogretmen, k, v)
        db.commit()
        db.refresh(db_ogretmen)
        return db_ogretmen
    except Exception as e:
        raise ValueError(f"Öğretmen güncellenirken hata oluştu: {str(e)}")

def delete_ogretmen(db: Session, id: UUID):
    db_ogretmen = get_ogretmen_by_id(db, id)
    if not db_ogretmen:
        return False
    try:
        db.delete(db_ogretmen)
        db.commit()
        return True
    except Exception as e:
        raise ValueError(f"Öğretmen silinirken hata oluştu: {str(e)}")

# Ders Programı CRUD İşlemleri
def create_ders_programi(db: Session, dp: DersProgramiCreate):
    try:
        db_dp = DersProgrami(**dp.dict())
        db.add(db_dp)
        db.commit()
        db.refresh(db_dp)
        return db_dp
    except Exception as e:
        raise ValueError(f"Ders programı oluşturulurken hata oluştu: {str(e)}")

def get_ders_programlari(db: Session):
    try:
        return db.query(DersProgrami).all()
    except Exception as e:
        raise ValueError(f"Ders programları listelenirken hata oluştu: {str(e)}")

def get_ders_programi_by_id(db: Session, id: UUID):
    try:
        return db.query(DersProgrami).filter(DersProgrami.id == str(id)).first()
    except Exception as e:
        raise ValueError(f"Ders programı getirilirken hata oluştu: {str(e)}")

def update_ders_programi(db: Session, id: UUID, dp: DersProgramiUpdate):
    db_dp = get_ders_programi_by_id(db, id)
    if not db_dp:
        return None
    try:
        for k, v in dp.dict(exclude_unset=True).items():
            setattr(db_dp, k, v)
        db.commit()
        db.refresh(db_dp)
        return db_dp
    except Exception as e:
        raise ValueError(f"Ders programı güncellenirken hata oluştu: {str(e)}")

def delete_ders_programi(db: Session, id: UUID):
    db_dp = get_ders_programi_by_id(db, id)
    if not db_dp:
        return False
    try:
        db.delete(db_dp)
        db.commit()
        return True
    except Exception as e:
        raise ValueError(f"Ders programı silinirken hata oluştu: {str(e)}")
