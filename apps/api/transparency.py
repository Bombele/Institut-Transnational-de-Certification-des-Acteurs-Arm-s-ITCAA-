# apps/api/routers/transparency.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.governance_models import FundingDisclosure, AuditExternal, AdvisoryMember

router = APIRouter(prefix="/transparency", tags=["transparency"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/overview")
def transparency_overview(db: Session = Depends(get_db)):
    funds = db.query(FundingDisclosure).filter_by(public=True).all()
    audits = db.query(AuditExternal).all()
    board = db.query(AdvisoryMember).filter_by(active=True).all()
    return {
        "funding": [{"funder": f.funder, "amount": f.amount, "year": f.year} for f in funds],
        "audits": [{"auditor": a.auditor_name, "scope": a.scope} for a in audits],
        "advisory_board": [{"name": m.name, "role": m.role.value, "region": m.region.value} for m in board]
    }
