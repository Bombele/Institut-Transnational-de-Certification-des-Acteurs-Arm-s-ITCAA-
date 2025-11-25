# apps/api/routers/ui.py
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/ui", tags=["ui"])
templates = Jinja2Templates(directory="templates")

@router.get("/map", response_class=HTMLResponse)
def map_page(request: Request):
    return templates.TemplateResponse("map.html", {"request": request})
# apps/api/routers/ui.py
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter(prefix="/ui", tags=["ui"])
templates = Jinja2Templates(directory="templates")

@router.get("/map", response_class=HTMLResponse)
def map_page(request: Request):
    return templates.TemplateResponse("map.html", {"request": request})
# apps/api/routers/ui.py
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.i18n import load_locale
from apps.api.models_cartography import Actor, Region, ActorType, ActorStatus
from apps.api.models_reports import AnnualReport
from apps.api.models_governance import AdvisoryMember, AdvisoryReport
from apps.api.models_diplomacy import Alliance
from apps.api.models_narration import CitizenNarration, NarrationType

router = APIRouter(prefix="/ui", tags=["ui"])
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def get_lang(request: Request):
    return request.query_params.get("lang") or "fr"

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    lang = get_lang(request); t = load_locale(lang)
    return templates.TemplateResponse("home.html", {"request": request, "t": t, "lang": lang})

@router.get("/map", response_class=HTMLResponse)
def map_page(request: Request, db: Session = Depends(get_db)):
    lang = get_lang(request); t = load_locale(lang)
    # Précharger liste d'acteurs minimal pour le sélecteur (id, name, type, region)
    actors = db.query(Actor.id, Actor.name, Actor.type, Actor.region).order_by(Actor.name).all()
    return templates.TemplateResponse("map.html", {"request": request, "t": t, "lang": lang, "actors": actors})

@router.get("/actors", response_class=HTMLResponse)
def actors_list(request: Request, db: Session = Depends(get_db),
                region: str | None = None, type: str | None = None, status: str | None = None, q: str | None = None,
                page: int = 1, per_page: int = 20):
    lang = get_lang(request); t = load_locale(lang)
    query = db.query(Actor)
    if region: query = query.filter(Actor.region == Region(region))
    if type: query = query.filter(Actor.type == ActorType(type))
    if status: query = query.filter(Actor.status == ActorStatus(status))
    if q: query = query.filter(Actor.name.ilike(f"%{q}%"))
    total = query.count()
    actors = query.order_by(Actor.name).offset((page-1)*per_page).limit(per_page).all()
    return templates.TemplateResponse("actors_list.html", {
        "request": request, "t": t, "lang": lang,
        "actors": actors, "total": total, "page": page, "per_page": per_page,
        "filters": {"region": region, "type": type, "status": status, "q": q}
    })

@router.get("/actors/{actor_id}", response_class=HTMLResponse)
def actor_detail(actor_id: int, request: Request, db: Session = Depends(get_db)):
    lang = get_lang(request); t = load_locale(lang)
    from apps.api.models_cartography import InfluenceZone, ActorRelation
    from apps.api.services.protocols_service import compute_scores_from_db
    actor = db.query(Actor).get(actor_id)
    if not actor:
        return templates.TemplateResponse("404.html", {"request": request, "t": t, "lang": lang}, status_code=404)
    zones = db.query(InfluenceZone).filter_by(actor_id=actor_id).all()
    relations = db.query(ActorRelation).filter_by(source_actor_id=actor_id).all()
    scores = compute_scores_from_db(db, actor_id)
    return templates.TemplateResponse("actor_detail.html", {
        "request": request, "t": t, "lang": lang, "actor": actor,
        "zones": zones, "relations": relations, "scores": scores
    })

@router.get("/reports", response_class=HTMLResponse)
def reports_library(request: Request, db: Session = Depends(get_db)):
    lang = get_lang(request); t = load_locale(lang)
    reports = db.query(AnnualReport).order_by(AnnualReport.year.desc()).all()
    return templates.TemplateResponse("reports.html", {"request": request, "t": t, "lang": lang, "reports": reports})

@router.get("/governance", response_class=HTMLResponse)
def governance_page(request: Request, db: Session = Depends(get_db)):
    lang = get_lang(request); t = load_locale(lang)
    members = db.query(AdvisoryMember).filter_by(active=True).all()
    advisory_reports = db.query(AdvisoryReport).filter_by(public=True).all()
    alliances = db.query(Alliance).filter_by(active=True).all()
    return templates.TemplateResponse("governance.html", {
        "request": request, "t": t, "lang": lang,
        "members": members, "advisory_reports": advisory_reports, "alliances": alliances
    })

@router.get("/lexcivic", response_class=HTMLResponse)
def lexcivic_page(request: Request, db: Session = Depends(get_db)):
    lang = get_lang(request); t = load_locale(lang)
    narrations = db.query(CitizenNarration).order_by(CitizenNarration.created_at.desc()).limit(100).all()
    return templates.TemplateResponse("lexcivic.html", {"request": request, "t": t, "lang": lang, "narrations": narrations})

@router.post("/lexcivic/submit", response_class=HTMLResponse)
def lexcivic_submit(request: Request, db: Session = Depends(get_db),
                    type: str = Form(...), content: str = Form(...), locale: str = Form(...), contributor: str = Form(...)):
    n = CitizenNarration(type=NarrationType(type), content=content, locale=locale, contributor=contributor)
    db.add(n); db.commit()
    lang = get_lang(request)
    return RedirectResponse(url=f"/ui/lexcivic?lang={lang}", status_code=302)
