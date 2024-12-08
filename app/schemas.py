# app/schemas.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

# --- Öğrenci Şemaları ---

class OgrenciBase(BaseModel):
    ad: str = Field(..., max_length=100, description="Öğrencinin adı")
    soyad: str = Field(..., max_length=100, description="Öğrencinin soyadı")
    ogrenci_numarasi: str = Field(..., max_length=50, description="Öğrenci numarası")
    sinif: str = Field(..., max_length=10, description="Sınıf")
    iletisim: EmailStr = Field(..., description="Öğrencinin e-posta adresi")

class OgrenciCreate(OgrenciBase):
    pass

class OgrenciUpdate(BaseModel):
    ad: Optional[str] = Field(None, max_length=100, description="Öğrencinin adı")
    soyad: Optional[str] = Field(None, max_length=100, description="Öğrencinin soyadı")
    ogrenci_numarasi: Optional[str] = Field(None, max_length=50, description="Öğrenci numarası")
    sinif: Optional[str] = Field(None, max_length=10, description="Sınıf")
    iletisim: Optional[EmailStr] = Field(None, description="Öğrencinin e-posta adresi")

class OgrenciRead(OgrenciBase):
    id: UUID
    kayit_tarihi: datetime
    guncelleme_tarihi: Optional[datetime]

    class Config:
        orm_mode = True

# --- Öğretmen Şemaları ---

class OgretmenBase(BaseModel):
    ad: str = Field(..., max_length=100, description="Öğretmenin adı")
    soyad: str = Field(..., max_length=100, description="Öğretmenin soyadı")
    brans: str = Field(..., max_length=100, description="Öğretmenin branşı")
    iletisim: EmailStr = Field(..., description="Öğretmenin e-posta adresi")
    ogretmen_numarasi: str = Field(..., max_length=50, description="Öğretmen numarası")  # Yeni alan

class OgretmenCreate(OgretmenBase):
    pass

class OgretmenUpdate(BaseModel):
    ad: Optional[str] = Field(None, max_length=100, description="Öğretmenin adı")
    soyad: Optional[str] = Field(None, max_length=100, description="Öğretmenin soyadı")
    brans: Optional[str] = Field(None, max_length=100, description="Öğretmenin branşı")
    iletisim: Optional[EmailStr] = Field(None, description="Öğretmenin e-posta adresi")
    ogretmen_numarasi: Optional[str] = Field(None, max_length=50, description="Öğretmen numarası")  # Yeni alan

class OgretmenRead(OgretmenBase):
    id: UUID
    kayit_tarihi: datetime
    guncelleme_tarihi: Optional[datetime]
    ders_programlari: List["DersProgramiRead"] = []
    
    class Config:
        orm_mode = True

# --- Ders Programı Şemaları ---

class DersProgramiBase(BaseModel):
    sinif: str = Field(..., max_length=10, description="Sınıf")
    ders: str = Field(..., max_length=100, description="Ders adı")
    saat: str = Field(..., max_length=20, description="Ders saati")
    ogretmen_id: UUID = Field(..., description="Öğretmen ID'si")

class DersProgramiCreate(DersProgramiBase):
    pass

class DersProgramiUpdate(BaseModel):
    sinif: Optional[str] = Field(None, max_length=10, description="Sınıf")
    ders: Optional[str] = Field(None, max_length=100, description="Ders adı")
    saat: Optional[str] = Field(None, max_length=20, description="Ders saati")
    ogretmen_id: Optional[UUID] = Field(None, description="Öğretmen ID'si")

class DersProgramiRead(DersProgramiBase):
    id: UUID
    kayit_tarihi: datetime
    guncelleme_tarihi: Optional[datetime]
    ogretmen: OgretmenRead
    
    class Config:
        orm_mode = True

# Geriye kalan ilişkisel referansların çözülmesi
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas import OgretmenRead, DersProgramiRead