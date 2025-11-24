# apps/api/routers/tracking.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.services.tracking_service import check_expiring_mous, check_expiring_mandates

router = APIRouter(prefix="/tracking", tags=["tracking"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/mous/expiring")
def expiring_mous(db: Session = Depends(get_db)):
    return [{"partner": m.partner_name, "expires_at": m.expires_at.isoformat()} for m in check_expiring_mous(db)]

@router.get("/mandates/expiring")
def expiring_mandates(db: Session = Depends(get_db)):
    return [{"member_id": m.member_id, "end_date": m.end_date.isoformat()} for m in check_expiring_mandates(db)]
