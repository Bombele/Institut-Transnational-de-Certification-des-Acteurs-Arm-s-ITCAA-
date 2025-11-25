# apps/api/routers/diplomatic_overview.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models_diplomacy import Alliance
from apps.api.models_governance import AdvisoryMember, AdvisoryReport
from apps.api.i18n import get_lang, load_locale

router = APIRouter(prefix="/diplomacy", tags=["diplomacy"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/overview")
def diplomatic_overview(request: Request, db: Session = Depends(get_db)):
    lang = get_lang(request); t = load_locale(lang)
    alliances = db.query(Alliance).filter_by(active=True).all()
    members = db.query(AdvisoryMember).filter_by(active=True).all()
    reports = db.query(AdvisoryReport).filter_by(public=True).all()
    return {
        "title": f"{t['app.title']} – Cadre diplomatique formel",
        "alliances_count": len(alliances),
        "advisory_members_count": len(members),
        "reports_count": len(reports),
        "lang": lang
    }
