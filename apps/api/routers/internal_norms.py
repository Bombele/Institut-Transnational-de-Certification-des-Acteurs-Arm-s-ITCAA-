from fastapi import APIRouter, HTTPException
import yaml
from pathlib import Path

router = APIRouter()

# Chemin vers les dictionnaires
DICTIONARIES_PATH = Path("data/dictionaries")

def load_yaml(file_name: str):
    file_path = DICTIONARIES_PATH / file_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Fichier {file_name} non trouvé")
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# Endpoint pour consulter les normes internes
@router.get("/internal-norms")
def get_internal_norms():
    return load_yaml("internal_norms.yml")

# Endpoint combiné avec DIH et légitimité
@router.get("/all")
def get_all_criteria():
    return {
        "dih_principles": load_yaml("dih_principles.yml"),
        "legitimacy_indicators": load_yaml("legitimacy_indicators.yml"),
        "internal_norms": load_yaml("internal_norms.yml")
    }
