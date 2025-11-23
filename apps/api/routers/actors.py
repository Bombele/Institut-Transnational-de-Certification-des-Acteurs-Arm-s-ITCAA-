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
