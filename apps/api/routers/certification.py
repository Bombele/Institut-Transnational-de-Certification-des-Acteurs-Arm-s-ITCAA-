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
from fastapi import APIRouter, Request
from apps.api.i18n import get_lang, load_locale

router = APIRouter(prefix="/certification", tags=["certification"])

# Exemple endpoint: capsule de certification d'un acteur
@router.get("/{actor_id}/capsule")
def get_capsule(actor_id: int, request: Request):
    lang = get_lang(request)
    t = load_locale(lang)

    # ⚖️ Exemple de calcul (ici simulé, normalement basé sur DB et scoring DIH/légitimité/normes)
    capsule = {
        "actor_id": actor_id,
        "scores": {
            "dih": 0.82,
            "legitimacy": 0.78,
            "norms": 0.71
        },
        "certification_score": 0.77,
        "version": "v2.0"
    }

    # 🔤 Labels traduits
    labels = {
        "dih": t["protocol.dih.title"],
        "legitimacy": t["protocol.legitimacy.title"],
        "norms": t["protocol.internal_norms.title"],
        "score": t["capsule.score"],
        "version": t["capsule.version"],
        "validations": t["capsule.validations"]
    }

    return {
        "labels": labels,
        "capsule": capsule,
        "lang": lang
    }


# Exemple endpoint: liste des acteurs certifiés
@router.get("/actors")
def list_actors(request: Request):
    lang = get_lang(request)
    t = load_locale(lang)

    # ⚖️ Exemple de données (normalement récupérées depuis la DB)
    actors = [
        {"id": 1, "name": "Forces de Résistance du Kivu", "score": 0.77},
        {"id": 2, "name": "Movimiento Humanitario Andino", "score": 0.81}
    ]

    return {
        "title": t["nav.actors"],
        "actors": actors,
        "lang": lang
    }
