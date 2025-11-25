# apps/api/routers/risks.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models_actors import RiskRegister, RiskType, RiskLevel

router = APIRouter(prefix="/risks", tags=["risks"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/")
def list_risks(db: Session = Depends(get_db), level: RiskLevel | None = None):
    q = db.query(RiskRegister)
    if level: q = q.filter(RiskRegister.level == level)
    return q.order_by(RiskRegister.reviewed_at.desc()).all()

@router.post("/")
def add_risk(payload: dict, db: Session = Depends(get_db)):
    r = RiskRegister(**payload); db.add(r); db.commit(); db.refresh(r); return r
