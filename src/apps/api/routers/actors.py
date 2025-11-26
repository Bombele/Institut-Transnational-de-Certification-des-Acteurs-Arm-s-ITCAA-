from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models.models_actors import Actor, ActorType, Region
from apps.api.schemas.schemas_actors import ActorCreate, ActorRead

router = APIRouter(prefix="/actors", tags=["Actors"])

# 🔌 Dépendance pour obtenir la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔍 Lister les acteurs avec filtres optionnels
@router.get("/", response_model=list[ActorRead])
def list_actors(
    db: Session = Depends(get_db),
    type: ActorType | None = Query(None, description="Filtrer par type d’acteur"),
    region: Region | None = Query(None, description="Filtrer par région"),
    q: str | None = Query(None, description="Recherche par nom")
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
@router.post("/", response_model=ActorRead, status_code=201)
def create_actor(payload: ActorCreate, db: Session = Depends(get_db)):
    actor = Actor(**payload.dict())
    db.add(actor)
    db.commit()
    db.refresh(actor)
    return actor

# 🔎 Obtenir un acteur par ID
@router.get("/{actor_id}", response_model=ActorRead)
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = db.query(Actor).filter(Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Acteur non trouvé")
    return actor
