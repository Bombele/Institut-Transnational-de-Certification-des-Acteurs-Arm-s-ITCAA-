from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from apps.api.models.models_actors import Base  # adapte selon l’emplacement réel de tes modèles

# 📦 URL de la base (SQLite locale ou PostgreSQL en production)
DATABASE_URL = "sqlite:///./itcaa.db"  # pour PostgreSQL : "postgresql://user:password@host/dbname"

# ⚙️ Création du moteur SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# 🧠 Session locale pour FastAPI
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🛠️ Fonction d’initialisation de la base
def init_db():
    Base.metadata.create_all(bind=engine)
