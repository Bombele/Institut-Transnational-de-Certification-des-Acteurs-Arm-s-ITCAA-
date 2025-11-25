from pathlib import Path
import yaml
from db import models

DICTIONARIES_PATH = Path("data/dictionaries")

def load_internal_norms():
    file_path = DICTIONARIES_PATH / "internal_norms.yml"
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["internal_norms"]

def compute_internal_norms_score(actor: models.Actor) -> float:
    """
    Calcule le score basé sur les normes internes créées par l'acteur.
    """
    norms = load_internal_norms()
    base_score = sum(norms.values()) / len(norms)

    # Bonus si l’acteur a documenté des engagements normatifs
    bonus = 0.0
    if actor.engagements:
        for e in actor.engagements:
            if e.category == "norms":
                bonus += 0.1
            elif e.category == "discipline":
                bonus += 0.05

    return round(min(base_score + bonus, 1.0), 2)
