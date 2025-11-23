from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import models, session
from services import dih_score, legitimacy

router = APIRouter()

# Dependencia para obtener la sesión DB
def get_db():
    db = session.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Calcular score de certificación para un actor
@router.post("/{actor_id}/calculate")
def calculate_certification(actor_id: int, db: Session = Depends(get_db)):
    # Verificar que el actor existe
    actor = db.query(models.Actor).filter(models.Actor.id == actor_id).first()
    if not actor:
        raise HTTPException(status_code=404, detail="Actor no encontrado")

    # Calcular los scores parciales
    dih = dih_score.compute_dih_score(actor)
    legit = legitimacy.compute_legitimacy_score(actor)

    # Fórmula de certificación (puedes ajustar los pesos)
    certification_score = round((dih * 0.5 + legit * 0.5), 2)

    # Crear cápsula automática
    capsule = models.Capsule(
        actor_id=actor.id,
        narrative=f"Certificación calculada para {actor.name}",
        legitimacy_score=legit,
        dih_score=dih,
        certification_score=certification_score,
        version="v1.0",
        validations=[{"source": "ITCAA", "status": "calculado"}],
    )
    db.add(capsule)
    db.commit()
    db.refresh(capsule)

    return {
        "actor": actor.name,
        "dih_score": dih,
        "legitimacy_score": legit,
        "certification_score": certification_score,
        "capsule_id": capsule.id,
  }
