from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, schemas, session

router = APIRouter()

# Dépendance pour obtenir la session DB
def get_db():
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ajouter un acteur
@router.post("/", response_model=schemas.ActorOut)
def create_actor(actor: schemas.ActorCreate, db: Session = Depends(get_db)):
    db_actor = models.Actor(**actor.dict())
    db.add(db_actor)
    db.commit()
    db.refresh(db_actor)
    return db_actor

# Lister tous les acteurs
@router.get("/", response_model=list[schemas.ActorOut])
def list_actors(db: Session = Depends(get_db)):
    return db.query(models.Actor).all()

# Obtenir un acteur par ID
@router.get("/{actor_id}", response_model=schemas.ActorOut)
def get_actor(actor_id: int, db: Session = Depends(get_db)):
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Acteur non trouvé")
    return actor
# apps/api/routers/actors.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models_actors import Actor, ActorType, Region

router = APIRouter(prefix="/actors", tags=["actors"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/")
def list_actors(
    db: Session = Depends(get_db),
    type: ActorType | None = Query(None),
    region: Region | None = Query(None),
    q: str | None = Query(None)
):
    query = db.query(Actor)
    if type: query = query.filter(Actor.type == type)
    if region: query = query.filter(Actor.region == region)
    if q: query = query.filter(Actor.name.ilike(f"%{q}%"))
    return query.order_by(Actor.name).all()

@router.post("/")
def create_actor(payload: dict, db: Session = Depends(get_db)):
    a = Actor(**payload); db.add(a); db.commit(); db.refresh(a); return a
