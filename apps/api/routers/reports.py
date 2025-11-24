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
# apps/api/routers/export.py
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session
import csv, io
from apps.api.database import SessionLocal
from apps.api.models_cartography import Actor

router = APIRouter(prefix="/export", tags=["export"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/actors/json")
def export_json(db: Session = Depends(get_db)):
    actors = db.query(Actor).all()
    data = [
        {
            "id": a.id,
            "name": a.name,
            "type": a.type.value,
            "region": a.region.value,
            "status": a.status.value,
            "aliases": a.aliases,
            "languages": a.languages
        }
        for a in actors
    ]
    return JSONResponse(content=data)

@router.get("/actors/csv")
def export_csv(db: Session = Depends(get_db)):
    actors = db.query(Actor).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id","name","type","region","status","aliases","languages"])
    for a in actors:
        writer.writerow([a.id, a.name, a.type.value, a.region.value, a.status.value, ";".join(a.aliases or []), ";".join(a.languages or [])])
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition":"attachment; filename=actors.csv"})
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from apps.api.database import SessionLocal
from apps.api.models_cartography import Actor, InfluenceZone, ActorRelation
from apps.api.services.protocols_service import compute_scores_from_db
from apps.api.services.pdf_service import render_pdf
from apps.api.i18n import get_lang, load_locale

router = APIRouter(prefix="/reports", tags=["reports"])
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/actor/{actor_id}/pdf")
def actor_report_pdf(actor_id: int, request: Request, db: Session = Depends(get_db)):
    lang = get_lang(request); t = load_locale(lang)
    actor = db.query(Actor).get(actor_id)
    if not actor: return {"error":"not_found"}
    zones = db.query(InfluenceZone).filter_by(actor_id=actor_id).all()
    relations = db.query(ActorRelation).filter_by(source_actor_id=actor_id).all()
    scores = compute_scores_from_db(db, actor_id)

    html_content = templates.get_template("report.html").render(
        title=f"{t['app.title']} – Rapport de certification",
        actor={"name": actor.name, "type": actor.type.value, "region": actor.region.value, "status": actor.status.value},
        scores=scores,
        zones=zones,
        relations=relations,
        labels=t,
        lang=lang
    )
    return render_pdf(html_content, filename=f"actor_{actor_id}_report.pdf")
