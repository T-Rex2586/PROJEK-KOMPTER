"""
Script untuk mengisi data awal (seed) ke database.
Jalankan: python seed.py
Tabel: tblmhs, tbldosen, tblmk, tblkul
"""
from sqlalchemy.orm import Session
from backend.database import engine, Base
from backend.models import Mahasiswa, Dosen, Matakuliah, Perkuliahan


def seed():
    # Buat tabel yang belum ada
    Base.metadata.create_all(bind=engine)

    db = Session(bind=engine)

    try:
        # === DATA MAHASISWA (tblmhs) ===
        mahasiswa_data = [
            Mahasiswa(nim="MHS001", nama="Ahmad Rizki Pratama", alamat="Jl. Merdeka No. 10, Semarang"),
            Mahasiswa(nim="MHS002", nama="Siti Nurhaliza Putri", alamat="Jl. Diponegoro No. 25, Yogyakarta"),
            Mahasiswa(nim="MHS003", nama="Bagas Adi Nugroho", alamat="Jl. Sudirman No. 8, Solo"),
            Mahasiswa(nim="MHS004", nama="Dewi Safitri Anggraeni", alamat="Jl. Ahmad Yani No. 15, Magelang"),
            Mahasiswa(nim="MHS005", nama="Rizky Ramadhan Putra", alamat="Jl. Pahlawan No. 3, Klaten"),
        ]

        for mhs in mahasiswa_data:
            exists = db.query(Mahasiswa).filter_by(nim=mhs.nim).first()
            if not exists:
                db.add(mhs)

        # === DATA DOSEN (tbldosen) ===
        dosen_data = [
            Dosen(nip="DSN001", nama="Dr. Hendra Wijaya, M.Kom.", alamat="Jl. Gatot Subroto No. 12, Semarang"),
            Dosen(nip="DSN002", nama="Prof. Sri Mulyani, S.Si., M.Sc.", alamat="Jl. Veteran No. 5, Yogyakarta"),
            Dosen(nip="DSN003", nama="Ir. Bambang Sutrisno, M.T.", alamat="Jl. Pemuda No. 20, Solo"),
            Dosen(nip="DSN004", nama="Dr. Ratna Sari Dewi, M.Pd.", alamat="Jl. Pandanaran No. 8, Semarang"),
            Dosen(nip="DSN005", nama="Agus Prasetyo, S.Kom., M.Cs.", alamat="Jl. Slamet Riyadi No. 15, Klaten"),
        ]

        for dsn in dosen_data:
            exists = db.query(Dosen).filter_by(nip=dsn.nip).first()
            if not exists:
                db.add(dsn)

        # === DATA MATAKULIAH (tblmk) ===
        matakuliah_data = [
            Matakuliah(kode="MK001", namamatkul="Pemrograman Web", sks=3, semester=3),
            Matakuliah(kode="MK002", namamatkul="Basis Data Lanjut", sks=3, semester=4),
            Matakuliah(kode="MK003", namamatkul="Jaringan Komputer", sks=3, semester=5),
            Matakuliah(kode="MK004", namamatkul="Algoritma & Struktur Data", sks=4, semester=2),
            Matakuliah(kode="MK005", namamatkul="Kecerdasan Buatan", sks=3, semester=6),
        ]

        for mk in matakuliah_data:
            exists = db.query(Matakuliah).filter_by(kode=mk.kode).first()
            if not exists:
                db.add(mk)

        db.commit()

        # === DATA KRS / PERKULIAHAN (tblkul) ===
        krs_data = [
            {"nim": "MHS001", "nip": "DSN001", "kode": "MK001", "nilai": "A"},
            {"nim": "MHS001", "nip": "DSN002", "kode": "MK002", "nilai": "B+"},
            {"nim": "MHS002", "nip": "DSN001", "kode": "MK001", "nilai": "A-"},
            {"nim": "MHS002", "nip": "DSN003", "kode": "MK003", "nilai": None},
            {"nim": "MHS003", "nip": "DSN004", "kode": "MK004", "nilai": "B"},
            {"nim": "MHS003", "nip": "DSN005", "kode": "MK005", "nilai": None},
            {"nim": "MHS004", "nip": "DSN002", "kode": "MK002", "nilai": "A"},
            {"nim": "MHS005", "nip": "DSN001", "kode": "MK001", "nilai": "B+"},
        ]

        for krs in krs_data:
            exists = db.query(Perkuliahan).filter_by(nim=krs["nim"], kode=krs["kode"]).first()
            if not exists:
                db.add(Perkuliahan(
                    nim=krs["nim"],
                    nip=krs["nip"],
                    kode=krs["kode"],
                    nilai=krs["nilai"],
                ))

        db.commit()
        print("[OK] Seed data berhasil dimasukkan!")

        # Print summary
        print(f"   Mahasiswa  : {db.query(Mahasiswa).count()} data")
        print(f"   Dosen      : {db.query(Dosen).count()} data")
        print(f"   Matakuliah : {db.query(Matakuliah).count()} data")
        print(f"   KRS        : {db.query(Perkuliahan).count()} data")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error saat seed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
