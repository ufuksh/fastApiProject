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
    db_ogrenci = Ogrenci(**ogrenci.dict())
    db.add(db_ogrenci)
    db.commit()
    db.refresh(db_ogrenci)
    return db_ogrenci

def get_ogrenciler(db: Session):
    return db.query(Ogrenci).all()

def get_ogrenci_by_id(db: Session, id: UUID):
    return db.query(Ogrenci).filter(Ogrenci.id == str(id)).first()

def update_ogrenci(db: Session, id: UUID, ogrenci: OgrenciUpdate):
    db_ogrenci = get_ogrenci_by_id(db, id)
    if not db_ogrenci:
        return None
    for k, v in ogrenci.dict(exclude_unset=True).items():
        setattr(db_ogrenci, k, v)
    db.commit()
    db.refresh(db_ogrenci)
    return db_ogrenci

def delete_ogrenci(db: Session, id: UUID):
    db_ogrenci = get_ogrenci_by_id(db, id)
    if db_ogrenci:
        db.delete(db_ogrenci)
        db.commit()
        return True
    return False

# Öğretmen CRUD İşlemleri
def create_ogretmen(db: Session, ogretmen: OgretmenCreate):
    db_ogretmen = Ogretmen(**ogretmen.dict())
    db.add(db_ogretmen)
    db.commit()
    db.refresh(db_ogretmen)
    return db_ogretmen

def get_ogretmenler(db: Session):
    return db.query(Ogretmen).all()

def get_ogretmen_by_id(db: Session, id: UUID):
    return db.query(Ogretmen).filter(Ogretmen.id == str(id)).first()

def update_ogretmen(db: Session, id: UUID, ogretmen: OgretmenUpdate):
    db_ogretmen = get_ogretmen_by_id(db, id)
    if not db_ogretmen:
        return None
    for k, v in ogretmen.dict(exclude_unset=True).items():
        setattr(db_ogretmen, k, v)
    db.commit()
    db.refresh(db_ogretmen)
    return db_ogretmen

def delete_ogretmen(db: Session, id: UUID):
    db_ogretmen = get_ogretmen_by_id(db, id)
    if db_ogretmen:
        db.delete(db_ogretmen)
        db.commit()
        return True
    return False

# Ders Programı CRUD İşlemleri
def create_ders_programi(db: Session, dp: DersProgramiCreate):
    db_dp = DersProgrami(**dp.dict())
    db.add(db_dp)
    db.commit()
    db.refresh(db_dp)
    return db_dp

def get_ders_programlari(db: Session):
    return db.query(DersProgrami).all()

def get_ders_programi_by_id(db: Session, id: UUID):
    return db.query(DersProgrami).filter(DersProgrami.id == str(id)).first()

def update_ders_programi(db: Session, id: UUID, dp: DersProgramiUpdate):
    db_dp = get_ders_programi_by_id(db, id)
    if not db_dp:
        return None
    for k, v in dp.dict(exclude_unset=True).items():
        setattr(db_dp, k, v)
    db.commit()
    db.refresh(db_dp)
    return db_dp

def delete_ders_programi(db: Session, id: UUID):
    db_dp = get_ders_programi_by_id(db, id)
    if db_dp:
        db.delete(db_dp)
        db.commit()
        return True
    return False
