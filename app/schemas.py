from pydantic import BaseModel
from typing import Optional
from uuid import UUID

# Öğrenci Şemaları
class OgrenciBase(BaseModel):
    ad: str
    soyad: str
    ogrenci_numarasi: str
    sinif: str
    iletisim: str

class OgrenciCreate(OgrenciBase):
    pass

class OgrenciUpdate(BaseModel):
    ad: Optional[str] = None
    soyad: Optional[str] = None
    ogrenci_numarasi: Optional[str] = None
    sinif: Optional[str] = None
    iletisim: Optional[str] = None

class OgrenciRead(OgrenciBase):
    id: UUID

    class Config:
        orm_mode = True


# Öğretmen Şemaları
class OgretmenBase(BaseModel):
    ad: str
    soyad: str
    brans: str
    iletisim: str

class OgretmenCreate(OgretmenBase):
    pass

class OgretmenUpdate(BaseModel):
    ad: Optional[str] = None
    soyad: Optional[str] = None
    brans: Optional[str] = None
    iletisim: Optional[str] = None

class OgretmenRead(OgretmenBase):
    id: UUID

    class Config:
        orm_mode = True


# Ders Programı Şemaları
class DersProgramiBase(BaseModel):
    sinif: str
    ders: str
    saat: str
    ogretmen_id: UUID

class DersProgramiCreate(DersProgramiBase):
    pass

class DersProgramiUpdate(BaseModel):
    sinif: Optional[str] = None
    ders: Optional[str] = None
    saat: Optional[str] = None
    ogretmen_id: Optional[UUID] = None

class DersProgramiRead(DersProgramiBase):
    id: UUID

    class Config:
        orm_mode = True
