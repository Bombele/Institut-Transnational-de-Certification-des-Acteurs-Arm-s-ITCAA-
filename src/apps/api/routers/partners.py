from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models.models_actors import Partner
from apps.api.schemas.schemas_actors import PartnerCreate, PartnerRead

router = APIRouter(prefix="/partners", tags=["Partners"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[PartnerRead])
def list_partners(db: Session = Depends(get_db)):
    return db.query(Partner).order_by(Partner.name).all()

@router.post("/", response_model=PartnerRead, status_code=201)
def create_partner(payload: PartnerCreate, db: Session = Depends(get_db)):
    partner = Partner(**payload.dict())
    db.add(partner)
    db.commit()
    db.refresh(partner)
    return partner

@router.get("/{partner_id}", response_model=PartnerRead)
def get_partner(partner_id: int, db: Session = Depends(get_db)):
    partner = db.query(Partner).filter(Partner.id == partner_id).first()
    if not partner:
        raise HTTPException(status_code=404, detail="Partenaire non trouvé")
    return partner
