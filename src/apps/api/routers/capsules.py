from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, schemas, session

router = APIRouter()

# Dependencia para obtener la sesión DB
def get_db():
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear una cápsula asociada a un actor
@router.post("/", response_model=schemas.CapsuleBase)
def create_capsule(actor_id: int, capsule: schemas.CapsuleBase, db: Session = Depends(get_db)):
    # Verificar que el actor existe
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor no encontrado")

    db_capsule = models.Capsule(actor_id=actor_id, **capsule.dict())
    db.add(db_capsule)
    db.commit()
    db.refresh(db_capsule)
    return db_capsule

# Listar todas las cápsulas
@router.get("/", response_model=list[schemas.CapsuleBase])
def list_capsules(db: Session = Depends(get_db)):
    return db.query(models.Capsule).all()

# Obtener cápsula por ID
@router.get
