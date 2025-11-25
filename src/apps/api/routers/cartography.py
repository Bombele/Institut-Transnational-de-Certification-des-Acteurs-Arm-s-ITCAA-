# apps/api/routers/cartography.py
from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models_cartography import Actor, Region, ActorType, ActorStatus, InfluenceZone, ActorRelation, ActorScore
from apps.api.services.protocols_service import compute_scores_from_db
from apps.api.i18n import get_lang, load_locale

router = APIRouter(prefix="/cartography", tags=["cartography"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/actors")
def list_actors(
    db: Session = Depends(get_db),
    type: ActorType | None = Query(None),
    region: Region | None = Query(None),
    status: ActorStatus | None = Query(None),
    q: str | None = Query(None)
):
    query = db.query(Actor)
    if type: query = query.filter(Actor.type == type)
    if region: query = query.filter(Actor.region == region)
    if status: query = query.filter(Actor.status == status)
    if q: query = query.filter(Actor.name.ilike(f"%{q}%"))
    return query.order_by(Actor.name).all()

@router.get("/actors/{actor_id}/profile")
def actor_profile(actor_id: int, request: Request, db: Session = Depends(get_db)):
    lang = get_lang(request); t = load_locale(lang)
    actor = db.query(Actor).get(actor_id)
    if not actor: return {"error": "not_found"}
    zones = db.query(InfluenceZone).filter_by(actor_id=actor_id).all()
    relations = db.query(ActorRelation).filter_by(source_actor_id=actor_id).all()
    # Scores agrégés
    scores = compute_scores_from_db(db, actor_id)
    return {
        "labels": {
            "name": t["actor.name"], "type": t["actor.type"], "region": t["actor.region"], "status": t["actor.status"],
            "scores": t["capsule.score"]
        },
        "actor": actor,
        "zones_count": len(zones),
        "relations": [{"target": r.target_name, "type": r.relation_type.value} for r in relations],
        "scores": scores,
        "lang": lang
    }

@router.get("/actors/{actor_id}/geojson")
def actor_geojson(actor_id: int, db: Session = Depends(get_db)):
    zones = db.query(InfluenceZone).filter_by(actor_id=actor_id).all()
    features = []
    for z in zones:
        if z.geojson and z.geojson.get("type") == "FeatureCollection":
            features += z.geojson["features"]
    return {"type": "FeatureCollection", "features": features}

@router.post("/actors/{actor_id}/zones")
def add_zone(actor_id: int, payload: dict, db: Session = Depends(get_db)):
    z = InfluenceZone(actor_id=actor_id, country=payload.get("country"), province=payload.get("province"),
                      cross_border=payload.get("cross_border", False), geojson=payload.get("geojson"))
    db.add(z); db.commit(); db.refresh(z); return z
