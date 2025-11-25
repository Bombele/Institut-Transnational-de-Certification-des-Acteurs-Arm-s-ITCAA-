from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from apps.api.database import SessionLocal
from apps.api.models_cartography import Actor, Region, ActorType
from apps.api.econ_service import annual_totals
from apps.api.governance_models import RiskRegister, AuditExternal
from apps.api.services.annual_report_service import render_annual_pdf
from apps.api.i18n import get_lang, load_locale

router = APIRouter(prefix="/annual", tags=["annual"])
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/report/{year}/pdf")
def annual_report(year: int, request: Request, db: Session = Depends(get_db)):
    lang = get_lang(request); t = load_locale(lang)

    # Portfolio par région/type
    portfolio = {}
    for r in Region:
        portfolio[r.value] = {t.value: db.query(Actor).filter(Actor.region==r, Actor.type==t).count() for t in ActorType}

    # Économie
    econ = annual_totals(db)

    # Risques
    risks = db.query(RiskRegister).all()

    # Audits externes
    audits = db.query(AuditExternal).all()

    html_content = templates.get_template("annual_report.html").render(
        title=f"{t['app.title']} – Rapport annuel consolidé",
        year=year,
        portfolio=portfolio,
        economics=econ,
        risks=risks,
        audits=audits,
        lang=lang
    )
    return render_annual_pdf(html_content, year)
