# apps/api/routers/reports.py
@router.get("/certification/{actor_id}/public-report")
def public_report(actor_id: int, request: Request):
    lang = get_lang(request); t = load_locale(lang)
    capsule = get_capsule_data(actor_id)  # scores + version + proofs count
    return {
        "title": f"{t['app.title']} – {t['capsule.score']}",
        "actor_id": actor_id,
        "scores": capsule["scores"],
        "version": capsule["version"],
        "proofs_count": capsule["proofs_count"],
        "lang": lang
    }
# apps/api/routers/reports.py
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.i18n import get_lang, load_locale
from apps.api.econ_service import annual_totals, simulate_baseline

router = APIRouter(prefix="/reports", tags=["reports"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/institutional")
def institutional_report(request: Request, db: Session = Depends(get_db)):
    lang = get_lang(request); t = load_locale(lang)
    econ = annual_totals(db)
    sim = simulate_baseline()
    return {
        "title": f"{t['app.title']} – Rapport institutionnel",
        "economics": {
            "totals": econ,
            "projection_baseline": sim
        },
        "lang": lang
}
# apps/api/routers/reports.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.i18n import get_lang, load_locale
from apps.api.actor_service import classify_portfolio, region_breakdown
from apps.api.econ_service import annual_totals, simulate_baseline

router = APIRouter(prefix="/reports", tags=["reports"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/institutional")
def institutional_report(request: Request, db: Session = Depends(get_db)):
    lang = get_lang(request); t = load_locale(lang)
    portfolio = classify_portfolio(db)
    regions = region_breakdown(db)
    econ = annual_totals(db)
    sim = simulate_baseline()
    return {
        "title": f"{t['app.title']} – Rapport institutionnel",
        "portfolio": {"counts": portfolio, "regions": regions},
        "economics": {"totals": econ, "projection_baseline": sim},
        "risks_summary": "Voir /risks pour le registre détaillé",
        "lang": lang
    }
# apps/api/routers/reports.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.i18n import get_lang, load_locale
from apps.api.models_cartography import Actor, Region, ActorType
from apps.api.services.protocols_service import compute_scores_from_db

router = APIRouter(prefix="/reports", tags=["reports"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/actor/{actor_id}")
def actor_report(actor_id: int, request: Request, db: Session = Depends(get_db)):
    lang = get_lang(request); t = load_locale(lang)
    actor = db.query(Actor).get(actor_id)
    if not actor: return {"error":"not_found"}
    scores = compute_scores_from_db(db, actor_id)
    return {
        "title": f"{t['app.title']} – {t['capsule.score']}",
        "actor": {"name": actor.name, "type": actor.type.value, "region": actor.region.value, "status": actor.status.value},
        "scores": {
            t["protocol.dih.title"]: round(scores["dih"],2),
            t["protocol.legitimacy.title"]: round(scores["legitimacy"],2),
            t["protocol.internal_norms.title"]: round(scores["norms"],2),
            t["capsule.score"]: round(scores["total"],2)
        },
        "status": scores["status"],
        "version": scores["version"],
        "lang": lang
}
