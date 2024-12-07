from pydantic import BaseModel
from typing import Optional, List

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
    id: int
    class Config:
        orm_mode = True

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
    id: int
    class Config:
        orm_mode = True

class DersProgramiBase(BaseModel):
    sinif: str
    ders: str
    saat: str
    ogretmen_id: int

class DersProgramiCreate(DersProgramiBase):
    pass

class DersProgramiUpdate(BaseModel):
    sinif: Optional[str] = None
    ders: Optional[str] = None
    saat: Optional[str] = None
    ogretmen_id: Optional[int] = None

class DersProgramiRead(DersProgramiBase):
    id: int
    class Config:
        orm_mode = True
