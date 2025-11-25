# apps/api/services/tracking_service.py
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from apps.api.models_tracking import MoU, Mandate

def check_expiring_mous(db: Session, days: int = 30):
    now = datetime.utcnow()
    threshold = now + timedelta(days=days)
    return db.query(MoU).filter(MoU.expires_at <= threshold, MoU.active == True).all()

def check_expiring_mandates(db: Session, days: int = 30):
    now = datetime.utcnow()
    threshold = now + timedelta(days=days)
    return db.query(Mandate).filter(Mandate.end_date <= threshold, Mandate.active == True).all()
