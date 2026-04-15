from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Mahasiswa(Base):
    """Tabel mahasiswa (tblmhs)"""
    __tablename__ = "tblmhs"

    nim = Column(String(20), primary_key=True)
    nama = Column(String(100))
    alamat = Column(String(255), nullable=True)

    perkuliahan = relationship("Perkuliahan", back_populates="mahasiswa")


class Dosen(Base):
    """Tabel dosen (tbldosen)"""
    __tablename__ = "tbldosen"

    nip = Column(String(20), primary_key=True)
    nama = Column(String(100))
    alamat = Column(String(255), nullable=True)

    perkuliahan = relationship("Perkuliahan", back_populates="dosen")


class Matakuliah(Base):
    """Tabel mata kuliah (tblmk)"""
    __tablename__ = "tblmk"

    kode = Column(String(10), primary_key=True)
    namamatkul = Column(String(100))
    sks = Column(Integer)
    semester = Column(Integer)

    perkuliahan = relationship("Perkuliahan", back_populates="matakuliah")


class Perkuliahan(Base):
    """Tabel kuliah/KRS (tblkul)"""
    __tablename__ = "tblkul"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nim = Column(String(20), ForeignKey("tblmhs.nim"))
    nip = Column(String(20), ForeignKey("tbldosen.nip"))
    kode = Column(String(10), ForeignKey("tblmk.kode"))
    nilai = Column(String(5), nullable=True)

    mahasiswa = relationship("Mahasiswa", back_populates="perkuliahan")
    dosen = relationship("Dosen", back_populates="perkuliahan")
    matakuliah = relationship("Matakuliah", back_populates="perkuliahan")