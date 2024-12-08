import uuid
from datetime import datetime
from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship
from app.database import Base  # Base'in doğru içe aktarıldığından emin olun


class Ogrenci(Base):
    __tablename__ = "ogrenciler"

    id = Column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    ad = Column(String(100), nullable=False, index=True)
    soyad = Column(String(100), nullable=False, index=True)
    ogrenci_numarasi = Column(String(50), unique=True, nullable=False, index=True)
    sinif = Column(String(10), nullable=False, index=True)
    iletisim = Column(String(255), nullable=False, index=True)
    kayit_tarihi = Column(DateTime, default=datetime.utcnow, nullable=False)
    guncelleme_tarihi = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    def __repr__(self):
        return (
            f"<Ogrenci(id={self.id}, ad={self.ad}, soyad={self.soyad}, "
            f"ogrenci_numarasi={self.ogrenci_numarasi})>"
        )


class Ogretmen(Base):
    __tablename__ = "ogretmenler"

    id = Column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    ad = Column(String(100), nullable=False, index=True)
    soyad = Column(String(100), nullable=False, index=True)
    brans = Column(String(100), nullable=False, index=True)
    iletisim = Column(String(255), nullable=False, index=True)
    kayit_tarihi = Column(DateTime, default=datetime.utcnow, nullable=False)
    guncelleme_tarihi = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # İlişkiler
    ders_programlari = relationship(
        "DersProgrami",
        back_populates="ogretmen",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return (
            f"<Ogretmen(id={self.id}, ad={self.ad}, soyad={self.soyad}, "
            f"brans={self.brans})>"
        )


class DersProgrami(Base):
    __tablename__ = "dersprogrami"

    id = Column(
        CHAR(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    sinif = Column(String(10), nullable=False, index=True)
    ders = Column(String(100), nullable=False, index=True)
    saat = Column(String(20), nullable=False, index=True)
    ogretmen_id = Column(
        CHAR(36),
        ForeignKey("ogretmenler.id"),
        nullable=False,
        index=True,
    )
    kayit_tarihi = Column(DateTime, default=datetime.utcnow, nullable=False)
    guncelleme_tarihi = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # İlişkiler
    ogretmen = relationship(
        "Ogretmen",
        back_populates="ders_programlari",
    )

    def __repr__(self):
        return (
            f"<DersProgrami(id={self.id}, sinif={self.sinif}, ders={self.ders}, "
            f"saat={self.saat}, ogretmen_id={self.ogretmen_id})>"
        )
