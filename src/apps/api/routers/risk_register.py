from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models.models_actors import RiskRegister
from apps.api.schemas.schemas_actors import RiskRegisterCreate, RiskRegisterRead

router = APIRouter(prefix="/risks", tags=["Risk Register"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[RiskRegisterRead])
def list_risks(db: Session = Depends(get_db)):
    return db.query(RiskRegister).order_by(RiskRegister.reviewed_at.desc()).all()

@router.post("/", response_model=RiskRegisterRead, status_code=201)
def create_risk(payload: RiskRegisterCreate, db: Session = Depends(get_db)):
    risk = RiskRegister(**payload.dict())
    db.add(risk)
    db.commit()
    db.refresh(risk)
    return risk

@router.get("/{risk_id}", response_model=RiskRegisterRead)
def get_risk(risk_id: int, db: Session = Depends(get_db)):
    risk = db.query(RiskRegister).filter(RiskRegister.id == risk_id).first()
    if not risk:
        raise HTTPException(status_code=404, detail="Risque non trouvé")
    return risk
