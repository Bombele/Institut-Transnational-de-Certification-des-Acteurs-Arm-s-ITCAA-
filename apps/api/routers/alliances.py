# apps/api/routers/alliances.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models_diplomacy import Alliance

router = APIRouter(prefix="/alliances", tags=["alliances"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/")
def list_alliances(db: Session = Depends(get_db)):
    return db.query(Alliance).all()

@router.post("/")
def add_alliance(payload: dict, db: Session = Depends(get_db)):
    a = Alliance(**payload)
    db.add(a); db.commit(); db.refresh(a)
    return a
