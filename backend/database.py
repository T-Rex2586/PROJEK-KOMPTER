from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Koneksi langsung ke SQL Server remote via Tailscale
# Login: admin_all (SQL Server Authentication)
SQLALCHEMY_DATABASE_URL = (
    "mssql+pyodbc://admin_all:PasswordKuat123!@100.103.74.76/kuliah"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()