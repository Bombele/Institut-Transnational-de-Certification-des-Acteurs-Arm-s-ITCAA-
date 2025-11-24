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
