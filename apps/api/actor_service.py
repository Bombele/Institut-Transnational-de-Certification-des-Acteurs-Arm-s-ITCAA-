# apps/api/actor_service.py
from sqlalchemy.orm import Session
from apps.api.models_actors import Actor, ActorType

def classify_portfolio(db: Session) -> dict:
    total = db.query(Actor).count()
    gane = db.query(Actor).filter(Actor.type == ActorType.GANE).count()
    pmc = db.query(Actor).filter(Actor.type == ActorType.PMC).count()
    militia = db.query(Actor).filter(Actor.type == ActorType.MILITIA).count()
    hybrid = db.query(Actor).filter(Actor.type == ActorType.HYBRID).count()
    return {"total": total, "gane": gane, "pmc": pmc, "militia": militia, "hybrid": hybrid}

def region_breakdown(db: Session) -> dict:
    # retourne un dict {region: count}
    from apps.api.models_actors import Region
    out = {}
    for r in Region:
        out[r.value] = db.query(Actor).filter(Actor.region == r).count()
    return out
