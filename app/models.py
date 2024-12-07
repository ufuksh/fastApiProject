import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from app.database import Base

class Ogrenci(Base):
    __tablename__ = "ogrenciler"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ad = Column(String(100), index=True)
    soyad = Column(String(100), index=True)
    ogrenci_numarasi = Column(String(50), unique=True, index=True)
    sinif = Column(String(10), index=True)
    iletisim = Column(String(255), index=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if isinstance(self.id, str):
            self.id = uuid.UUID(self.id)

class Ogretmen(Base):
    __tablename__ = "ogretmenler"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    ad = Column(String(100), index=True)
    soyad = Column(String(100), index=True)
    brans = Column(String(100), index=True)
    iletisim = Column(String(255), index=True)
    ders_programlari = relationship("DersProgrami", back_populates="ogretmen")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if isinstance(self.id, str):
            self.id = uuid.UUID(self.id)

class DersProgrami(Base):
    __tablename__ = "dersprogrami"
    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sinif = Column(String(10), index=True)
    ders = Column(String(100), index=True)
    saat = Column(String(20), index=True)
    ogretmen_id = Column(CHAR(36), ForeignKey("ogretmenler.id"))
    ogretmen = relationship("Ogretmen", back_populates="ders_programlari")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if isinstance(self.id, str):
            self.id = uuid.UUID(self.id)
