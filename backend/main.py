from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, joinedload
from typing import List
import models, schemas, database


app = FastAPI(title="SIAKAD API - Portal Akademik Kampus")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# STATISTIK DASHBOARD
# ==========================================
@app.get("/stats", response_model=schemas.StatsResponse)
def get_stats(db: Session = Depends(database.get_db)):
    return {
        "total_mahasiswa": db.query(models.Mahasiswa).count(),
        "total_dosen": db.query(models.Dosen).count(),
        "total_matakuliah": db.query(models.Matakuliah).count(),
        "total_krs": db.query(models.Perkuliahan).count(),
    }


# ==========================================
# FITUR CRUD DATA MAHASISWA (tblmhs)
# ==========================================
@app.get("/mahasiswa/", response_model=List[schemas.MahasiswaResponse])
def get_semua_mahasiswa(db: Session = Depends(database.get_db)):
    return db.query(models.Mahasiswa).all()


@app.post("/mahasiswa/")
def tambah_mahasiswa(req: schemas.MahasiswaCreate, db: Session = Depends(database.get_db)):
    exist = db.query(models.Mahasiswa).filter_by(nim=req.nim).first()
    if exist:
        raise HTTPException(status_code=400, detail="NIM sudah terdaftar!")

    baru = models.Mahasiswa(nim=req.nim, nama=req.nama, alamat=req.alamat)
    db.add(baru)
    db.commit()
    return {"message": "Data mahasiswa berhasil ditambahkan"}


@app.put("/mahasiswa/{nim}")
def update_mahasiswa(nim: str, req: schemas.MahasiswaBase, db: Session = Depends(database.get_db)):
    mhs = db.query(models.Mahasiswa).filter_by(nim=nim).first()
    if not mhs:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")
    mhs.nama = req.nama
    mhs.alamat = req.alamat
    db.commit()
    return {"message": "Data mahasiswa berhasil diupdate"}


@app.delete("/mahasiswa/{nim}")
def hapus_mahasiswa(nim: str, db: Session = Depends(database.get_db)):
    mhs = db.query(models.Mahasiswa).filter_by(nim=nim).first()
    if not mhs:
        raise HTTPException(status_code=404, detail="Mahasiswa tidak ditemukan")

    # Hapus juga data KRS milik mahasiswa ini agar tidak error relasi
    db.query(models.Perkuliahan).filter_by(nim=nim).delete()
    db.delete(mhs)
    db.commit()
    return {"message": "Data mahasiswa berhasil dihapus"}


# ==========================================
# FITUR CRUD DATA DOSEN (tbldosen)
# ==========================================
@app.get("/dosen/", response_model=List[schemas.DosenResponse])
def get_semua_dosen(db: Session = Depends(database.get_db)):
    return db.query(models.Dosen).all()


@app.post("/dosen/")
def tambah_dosen(req: schemas.DosenCreate, db: Session = Depends(database.get_db)):
    exist = db.query(models.Dosen).filter_by(nip=req.nip).first()
    if exist:
        raise HTTPException(status_code=400, detail="NIP sudah terdaftar!")
    baru = models.Dosen(nip=req.nip, nama=req.nama, alamat=req.alamat)
    db.add(baru)
    db.commit()
    return {"message": "Data dosen berhasil ditambahkan"}


@app.put("/dosen/{nip}")
def update_dosen(nip: str, req: schemas.DosenBase, db: Session = Depends(database.get_db)):
    dosen = db.query(models.Dosen).filter_by(nip=nip).first()
    if not dosen:
        raise HTTPException(status_code=404, detail="Dosen tidak ditemukan")
    dosen.nama = req.nama
    dosen.alamat = req.alamat
    db.commit()
    return {"message": "Data dosen berhasil diupdate"}


@app.delete("/dosen/{nip}")
def hapus_dosen(nip: str, db: Session = Depends(database.get_db)):
    dosen = db.query(models.Dosen).filter_by(nip=nip).first()
    if not dosen:
        raise HTTPException(status_code=404, detail="Dosen tidak ditemukan")
    # Hapus data KRS yang terkait dosen ini
    db.query(models.Perkuliahan).filter_by(nip=nip).delete()
    db.delete(dosen)
    db.commit()
    return {"message": "Data dosen berhasil dihapus"}


# ==========================================
# FITUR CRUD MATAKULIAH (tblmk)
# ==========================================
@app.get("/matakuliah/", response_model=List[schemas.MKBase])
def get_matakuliah(db: Session = Depends(database.get_db)):
    return db.query(models.Matakuliah).all()


@app.post("/matakuliah/")
def tambah_matakuliah(req: schemas.MKCreate, db: Session = Depends(database.get_db)):
    exist = db.query(models.Matakuliah).filter_by(kode=req.kode).first()
    if exist:
        raise HTTPException(status_code=400, detail="Kode matakuliah sudah terdaftar!")
    baru = models.Matakuliah(kode=req.kode, namamatkul=req.namamatkul, sks=req.sks, semester=req.semester)
    db.add(baru)
    db.commit()
    return {"message": "Matakuliah berhasil ditambahkan"}


@app.put("/matakuliah/{kode}")
def update_matakuliah(kode: str, req: schemas.MKUpdate, db: Session = Depends(database.get_db)):
    mk = db.query(models.Matakuliah).filter_by(kode=kode).first()
    if not mk:
        raise HTTPException(status_code=404, detail="Matakuliah tidak ditemukan")
    mk.namamatkul = req.namamatkul
    mk.sks = req.sks
    mk.semester = req.semester
    db.commit()
    return {"message": "Matakuliah berhasil diupdate"}


@app.delete("/matakuliah/{kode}")
def hapus_matakuliah(kode: str, db: Session = Depends(database.get_db)):
    mk = db.query(models.Matakuliah).filter_by(kode=kode).first()
    if not mk:
        raise HTTPException(status_code=404, detail="Matakuliah tidak ditemukan")
    db.query(models.Perkuliahan).filter_by(kode=kode).delete()
    db.delete(mk)
    db.commit()
    return {"message": "Matakuliah berhasil dihapus"}


# ==========================================
# FITUR KRS / PERKULIAHAN (tblkul)
# ==========================================
@app.get("/krs/", response_model=List[schemas.KRSResponse])
def get_semua_krs(db: Session = Depends(database.get_db)):
    """Ambil semua data KRS beserta relasi mahasiswa, dosen, dan matakuliah."""
    return (
        db.query(models.Perkuliahan)
        .options(
            joinedload(models.Perkuliahan.mahasiswa),
            joinedload(models.Perkuliahan.dosen),
            joinedload(models.Perkuliahan.matakuliah),
        )
        .all()
    )


@app.get("/krs/{nim}", response_model=List[schemas.KRSResponse])
def get_krs_mahasiswa(nim: str, db: Session = Depends(database.get_db)):
    """Ambil data KRS berdasarkan NIM mahasiswa."""
    return (
        db.query(models.Perkuliahan)
        .filter(models.Perkuliahan.nim == nim)
        .options(
            joinedload(models.Perkuliahan.mahasiswa),
            joinedload(models.Perkuliahan.dosen),
            joinedload(models.Perkuliahan.matakuliah),
        )
        .all()
    )


@app.post("/krs/")
def tambah_krs(req: schemas.KRSCreate, db: Session = Depends(database.get_db)):
    """Tambahkan data KRS baru (ambil matakuliah)."""
    # Validasi NIM
    mhs = db.query(models.Mahasiswa).filter_by(nim=req.nim).first()
    if not mhs:
        raise HTTPException(status_code=404, detail="Mahasiswa dengan NIM tersebut tidak ditemukan")

    # Validasi NIP
    dosen = db.query(models.Dosen).filter_by(nip=req.nip).first()
    if not dosen:
        raise HTTPException(status_code=404, detail="Dosen dengan NIP tersebut tidak ditemukan")

    # Validasi Kode MK
    mk = db.query(models.Matakuliah).filter_by(kode=req.kode).first()
    if not mk:
        raise HTTPException(status_code=404, detail="Matakuliah dengan kode tersebut tidak ditemukan")

    # Cek duplikat
    exist = db.query(models.Perkuliahan).filter_by(nim=req.nim, kode=req.kode).first()
    if exist:
        raise HTTPException(status_code=400, detail="Mahasiswa sudah mengambil matakuliah ini!")

    baru = models.Perkuliahan(nim=req.nim, nip=req.nip, kode=req.kode, nilai=req.nilai)
    db.add(baru)
    db.commit()
    return {"message": "KRS berhasil ditambahkan"}


@app.put("/krs/{id}")
def update_nilai_krs(id: int, req: schemas.KRSUpdate, db: Session = Depends(database.get_db)):
    """Update nilai KRS."""
    krs = db.query(models.Perkuliahan).filter_by(id=id).first()
    if not krs:
        raise HTTPException(status_code=404, detail="Data KRS tidak ditemukan")
    krs.nilai = req.nilai
    db.commit()
    return {"message": "Nilai KRS berhasil diupdate"}


@app.delete("/krs/{id}")
def hapus_krs(id: int, db: Session = Depends(database.get_db)):
    """Hapus data KRS."""
    krs = db.query(models.Perkuliahan).filter_by(id=id).first()
    if not krs:
        raise HTTPException(status_code=404, detail="Data KRS tidak ditemukan")
    db.delete(krs)
    db.commit()
    return {"message": "KRS berhasil dihapus"}