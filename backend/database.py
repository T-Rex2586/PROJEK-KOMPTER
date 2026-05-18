from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import os

host = os.getenv("DB_HOST", "100.103.74.76")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

if user and password:
    # SQL Server authentication
    SQLALCHEMY_DATABASE_URL = (
        f"mssql+pyodbc://{user}:{password}@{host}/kuliah"
        "?driver=ODBC+Driver+17+for+SQL+Server"
    )
else:
    # Windows Integrated authentication (fallback for local testing)
    SQLALCHEMY_DATABASE_URL = (
        f"mssql+pyodbc://@{host}/kuliah"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
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