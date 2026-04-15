from pydantic import BaseModel
from typing import Optional


# --- SKEMA MAHASISWA (tblmhs) ---
class MahasiswaBase(BaseModel):
    nama: str
    alamat: Optional[str] = None


class MahasiswaCreate(MahasiswaBase):
    nim: str


class MahasiswaResponse(MahasiswaCreate):
    class Config:
        from_attributes = True


# --- SKEMA DOSEN (tbldosen) ---
class DosenBase(BaseModel):
    nama: str
    alamat: Optional[str] = None


class DosenCreate(DosenBase):
    nip: str


class DosenResponse(DosenCreate):
    class Config:
        from_attributes = True


# --- SKEMA MATAKULIAH (tblmk) ---
class MKBase(BaseModel):
    kode: str
    namamatkul: str
    sks: int
    semester: int

    class Config:
        from_attributes = True


class MKCreate(BaseModel):
    kode: str
    namamatkul: str
    sks: int
    semester: int


class MKUpdate(BaseModel):
    namamatkul: str
    sks: int
    semester: int


# --- SKEMA PERKULIAHAN / KRS (tblkul) ---
class KRSCreate(BaseModel):
    nim: str
    nip: str
    kode: str
    nilai: Optional[str] = None


class KRSUpdate(BaseModel):
    nilai: Optional[str] = None


class KRSMahasiswaInfo(BaseModel):
    nim: str
    nama: str
    alamat: Optional[str] = None

    class Config:
        from_attributes = True


class KRSDosenInfo(BaseModel):
    nip: str
    nama: str

    class Config:
        from_attributes = True


class KRSMKInfo(BaseModel):
    kode: str
    namamatkul: str
    sks: int
    semester: int

    class Config:
        from_attributes = True


class KRSResponse(BaseModel):
    id: int
    nim: str
    nip: str
    kode: str
    nilai: Optional[str] = None
    mahasiswa: Optional[KRSMahasiswaInfo] = None
    dosen: Optional[KRSDosenInfo] = None
    matakuliah: Optional[KRSMKInfo] = None

    class Config:
        from_attributes = True


# --- SKEMA STATISTIK ---
class StatsResponse(BaseModel):
    total_mahasiswa: int
    total_dosen: int
    total_matakuliah: int
    total_krs: int