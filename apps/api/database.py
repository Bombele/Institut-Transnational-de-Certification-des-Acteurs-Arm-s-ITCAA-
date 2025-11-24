from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from apps.api.models import Base

DATABASE_URL = "sqlite:///./itcaa.db"  # ou PostgreSQL/MySQL selon ton choix

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Création des tables
def init_db():
    Base.metadata.create_all(bind=engine)
