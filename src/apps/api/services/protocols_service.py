# apps/api/services/protocols_service.py
import yaml
from pathlib import Path

def load_protocol(name: str):
    data = yaml.safe_load(Path(f"protocols/{name}.yml").read_text(encoding="utf-8"))
    return data  # {"version":...,"indicators":[...],"thresholds":{...}}

def aggregate(values, weights):
    return sum(v * w for v, w in zip(values, weights))

def compute_scores_from_db(db, actor_id: int):
    # Charger pondérations depuis YAML
    dih = load_protocol("dih")
    leg = load_protocol("legitimacy")
    nor = load_protocol("norms")

    # Récupérer valeurs des indicateurs depuis la DB (ex: DIHIndicator ou tables équivalentes pour leg/nor)
    from apps.api.models_cartography import DIHIndicator
    dih_rows = db.query(DIHIndicator).filter_by(actor_id=actor_id, version=dih["version"]).all()
    dih_values = [r.value for r in dih_rows] if dih_rows else [0.5]*len(dih["indicators"])
    dih_weights = [i["weight"] for i in dih["indicators"]]
    dih_score = aggregate(dih_values, dih_weights)

    # Démo simple pour légitimité et normes (tu peux créer des tables analogues)
    leg_values = [0.7]*len(leg["indicators"]); leg_weights = [i["weight"] for i in leg["indicators"]]
    nor_values = [0.6]*len(nor["indicators"]); nor_weights = [i["weight"] for i in nor["indicators"]]
    legitimacy_score = aggregate(leg_values, leg_weights)
    norms_score = aggregate(nor_values, nor_weights)

    total = round((dih_score + legitimacy_score + norms_score)/3, 4)
    certified_cut = (dih["thresholds"]["certified"] + leg["thresholds"]["certified"] + nor["thresholds"]["certified"]) / 3
    provisional_cut = (dih["thresholds"]["provisional"] + leg["thresholds"]["provisional"] + nor["thresholds"]["provisional"]) / 3
    status = "certified" if total >= certified_cut else ("provisional" if total >= provisional_cut else "not_certified")

    return {"dih": dih_score, "legitimacy": legitimacy_score, "norms": norms_score, "total": total, "status": status, "version": dih["version"]}
