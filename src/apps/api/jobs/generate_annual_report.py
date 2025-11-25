import datetime
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal, init_db
from apps.api.models_cartography import Actor, Region, ActorType
from apps.api.econ_service import annual_totals
from apps.api.governance_models import RiskRegister, AuditExternal
from apps.api.i18n import load_locale
from apps.api.services.annual_report_service import render_annual_pdf
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

def run(year: int, lang: str = "en"):
    init_db()
    db: Session = SessionLocal()

    # Portfolio par région/type
    portfolio = {}
    for r in Region:
        portfolio[r.value] = {t.value: db.query(Actor).filter(Actor.region==r, Actor.type==t).count() for t in ActorType}

    econ = annual_totals(db)
    risks = db.query(RiskRegister).all()
    audits = db.query(AuditExternal).all()
    t = load_locale(lang)

    html_content = templates.get_template("annual_report.html").render(
        title=f"{t['app.title']} – Annual consolidated report",
        year=year,
        portfolio=portfolio,
        economics=econ,
        risks=risks,
        audits=audits,
        lang=lang
    )

    return render_annual_pdf(html_content, year)
