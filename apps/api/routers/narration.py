# apps/api/routers/narration.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models_narration import CitizenNarration

router = APIRouter(prefix="/narration", tags=["narration"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/")
def list_narrations(db: Session = Depends(get_db)):
    return db.query(CitizenNarration).all()

@router.post("/")
def add_narration(payload: dict, db: Session = Depends(get_db)):
    n = CitizenNarration(**payload)
    db.add(n); db.commit(); db.refresh(n)
    return n
