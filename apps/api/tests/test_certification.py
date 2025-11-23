import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base
from db import models
from apps.api.main import app

# Configurer une base SQLite en mémoire pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer les tables
Base.metadata.create_all(bind=engine)

# Dépendance override pour utiliser la DB de test
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides = {}
app.dependency_overrides[lambda: None] = override_get_db  # simplification

client = TestClient(app)

@pytest.fixture
def db_session():
    """Fixture pour fournir une session DB propre à chaque test"""
    session = TestingSessionLocal()
    yield session
    session.close()

def test_certification_calculation(db_session):
    # 1. Créer un acteur
    actor = models.Actor(
        name="Forces de Résistance du Kivu",
        acronym="FRK",
        typology="GANE",
        country="RDC",
        region="Kivu",
        geojson={"type": "Point", "coordinates": [28.8, -2.4]}
    )
    db_session.add(actor)
    db_session.commit()
    db_session.refresh(actor)

    # 2. Appeler l’endpoint de certification
    response = client.post(f"/certification/{actor.id}/calculate")
    assert response.status_code == 200

    data = response.json()

    # 3. Vérifier les champs retournés
    assert data["actor"] == "Forces de Résistance du Kivu"
    assert "dih_score" in data
    assert "legitimacy_score" in data
    assert "certification_score" in data
    assert "capsule_id" in data
    assert isinstance(data["certification_score"], float)
