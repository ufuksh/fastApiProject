from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Ogrenci(Base):
    __tablename__ = "ogrenciler"
    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String(100), index=True)
    soyad = Column(String(100), index=True)
    ogrenci_numarasi = Column(String(50), unique=True, index=True)
    sinif = Column(String(10), index=True)
    iletisim = Column(String(255), index=True)

class Ogretmen(Base):
    __tablename__ = "ogretmenler"
    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String(100), index=True)
    soyad = Column(String(100), index=True)
    brans = Column(String(100), index=True)
    iletisim = Column(String(255), index=True)
    ders_programlari = relationship("DersProgrami", back_populates="ogretmen")

class DersProgrami(Base):
    __tablename__ = "dersprogrami"
    id = Column(Integer, primary_key=True, index=True)
    sinif = Column(String(10), index=True)
    ders = Column(String(100), index=True)
    saat = Column(String(20), index=True)
    ogretmen_id = Column(Integer, ForeignKey("ogretmenler.id"))
    ogretmen = relationship("Ogretmen", back_populates="ders_programlari")
