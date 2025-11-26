from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models_actors import Actor, ActorType, Region

router = APIRouter(prefix="/actors", tags=["Actors"])

# Dépendance pour obtenir la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔍 Lister les acteurs avec filtres optionnels
@router.get("/", response_model=list[Actor])
def list_actors(
    db: Session = Depends(get_db),
    type: ActorType | None = Query(None),
    region: Region | None = Query(None),
    q: str | None = Query(None)
):
    query = db.query(Actor)
    if type:
        query = query.filter(Actor.type == type)
    if region:
        query = query.filter(Actor.region == region)
    if q:
        query = query.filter(Actor.name.ilike(f"%{q}%"))
    return query.order_by(Actor.name).all()

# ➕ Créer un acteur
@router.post("/", response_model=Actor)
def create_actor(payload: dict, db: Session = Depends(get_db)):
    actor = Actor(**payload)
    db.add(actor)
    db.commit()
    db.refresh(actor)
    return actor

# 🔎 Obtenir un acteur par ID
@router.get("/{actor_id}", response_model=Actor)
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = db.query(Actor).filter(Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Acteur non trouvé")
    return actor
