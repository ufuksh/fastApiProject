from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Ogrenci(Base):
    __tablename__ = "ogrenciler"
    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, index=True)
    soyad = Column(String, index=True)
    ogrenci_numarasi = Column(String, unique=True, index=True)
    sinif = Column(String, index=True)
    iletisim = Column(String, index=True)

class Ogretmen(Base):
    __tablename__ = "ogretmenler"
    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, index=True)
    soyad = Column(String, index=True)
    brans = Column(String, index=True)
    iletisim = Column(String, index=True)
    ders_programlari = relationship("DersProgrami", back_populates="ogretmen")

class DersProgrami(Base):
    __tablename__ = "dersprogrami"
    id = Column(Integer, primary_key=True, index=True)
    sinif = Column(String, index=True)
    ders = Column(String, index=True)
    saat = Column(String, index=True)
    ogretmen_id = Column(Integer, ForeignKey("ogretmenler.id"))
    ogretmen = relationship("Ogretmen", back_populates="ders_programlari")
