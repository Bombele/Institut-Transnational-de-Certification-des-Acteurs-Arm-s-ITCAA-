# apps/api/routers/communication.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models_reports import AnnualReport
from apps.api.models_forums import ForumPresence
from apps.api.models_narration import CitizenNarration
from apps.api.i18n import get_lang, load_locale

router = APIRouter(prefix="/communication", tags=["communication"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/overview")
def communication_overview(request: Request, db: Session = Depends(get_db)):
    lang = get_lang(request); t = load_locale(lang)
    reports = db.query(AnnualReport).all()
    forums = db.query(ForumPresence).all()
    narrations = db.query(CitizenNarration).all()
    return {
        "title": f"{t['app.title']} – Communication & légitimité",
        "reports_count": len(reports),
        "forums_count": len(forums),
        "narrations_count": len(narrations),
        "lang": lang
    }
