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
import yaml
from pathlib import Path
from fastapi import APIRouter, Request
from apps.api.i18n import get_lang, load_locale

router = APIRouter(prefix="/certification", tags=["certification"])

# Fonction utilitaire pour charger un protocole YAML
def load_protocol(name: str):
    path = Path("protocols") / f"{name}.yml"
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# Calcul simple des scores (exemple simulé)
def compute_scores(actor_id: int):
    dih = load_protocol("dih")
    legitimacy = load_protocol("legitimacy")
    norms = load_protocol("norms")

    # ⚖️ Exemple : valeurs simulées pour chaque indicateur
    results = {
        "dih": sum(ind["weight"] * 0.82 for ind in dih["indicators"]),
        "legitimacy": sum(ind["weight"] * 0.78 for ind in legitimacy["indicators"]),
        "norms": sum(ind["weight"] * 0.71 for ind in norms["indicators"]),
    }
    total = (results["dih"] + results["legitimacy"] + results["norms"]) / 3
    status = "certified" if total >= 0.75 else "provisional" if total >= 0.6 else "not_certified"

    return {**results, "total": total, "status": status, "version": dih["version"]}

@router.get("/{actor_id}/report")
def get_report(actor_id: int, request: Request):
    lang = get_lang(request)
    t = load_locale(lang)

    scores = compute_scores(actor_id)

    return {
        "actor_id": actor_id,
        "scores": {
            t["protocol.dih.title"]: round(scores["dih"], 2),
            t["protocol.legitimacy.title"]: round(scores["legitimacy"], 2),
            t["protocol.internal_norms.title"]: round(scores["norms"], 2),
            t["capsule.score"]: round(scores["total"], 2)
        },
        "status": scores["status"],
        "version": scores["version"],
        "lang": lang
    }
# apps/api/routers/certification.py
import yaml
from pathlib import Path
from fastapi import APIRouter, Request
from apps.api.i18n import get_lang, load_locale

router = APIRouter(prefix="/certification", tags=["certification"])

def load_protocol(name: str):
    data = yaml.safe_load(Path(f"protocols/{name}.yml").read_text(encoding="utf-8"))
    return data["indicators"], data["thresholds"], data["version"]

def aggregate(values, weights):
    return sum(v*w for v, w in zip(values, weights))

def compute_from_protocols(actor_id: int):
    # Demo: valeurs simulées par indicateur (brancher DB/ML ensuite)
    dih_inds, dih_thr, version = load_protocol("dih")
    leg_inds, leg_thr, _ = load_protocol("legitimacy")
    nor_inds, nor_thr, _ = load_protocol("norms")

    dih_values = [0.82]*len(dih_inds); dih_weights = [i["weight"] for i in dih_inds]
    leg_values = [0.78]*len(leg_inds); leg_weights = [i["weight"] for i in leg_inds]
    nor_values = [0.71]*len(nor_inds); nor_weights = [i["weight"] for i in nor_inds]

    dih = aggregate(dih_values, dih_weights)
    leg = aggregate(leg_values, leg_weights)
    nor = aggregate(nor_values, nor_weights)
    total = round((dih + leg + nor)/3, 4)

    # Statut global: moyenne des seuils (simplifié)
    certified_cut = (dih_thr["certified"] + leg_thr["certified"] + nor_thr["certified"]) / 3
    provisional_cut = (dih_thr["provisional"] + leg_thr["provisional"] + nor_thr["provisional"]) / 3
    status = "certified" if total >= certified_cut else ("provisional" if total >= provisional_cut else "not_certified")

    return {"dih": dih, "legitimacy": leg, "norms": nor, "total": total, "status": status, "version": version}

@router.get("/{actor_id}/report")
def report(actor_id: int, request: Request):
    lang = get_lang(request); t = load_locale(lang)
    s = compute_from_protocols(actor_id)
    return {
        "actor_id": actor_id,
        "scores": {
            t["protocol.dih.title"]: round(s["dih"], 2),
            t["protocol.legitimacy.title"]: round(s["legitimacy"], 2),
            t["protocol.internal_norms.title"]: round(s["norms"], 2),
            t["capsule.score"]: round(s["total"], 2)
        },
        "status": s["status"],
        "version": s["version"],
        "lang": lang
    }
