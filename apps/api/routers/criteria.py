from fastapi import APIRouter, HTTPException
import yaml
from pathlib import Path

router = APIRouter()

# Ruta base de los diccionarios
DICTIONARIES_PATH = Path("data/dictionaries")

def load_yaml(file_name: str):
    file_path = DICTIONARIES_PATH / file_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Archivo {file_name} no encontrado")
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

# Endpoint para criterios DIH
@router.get("/dih")
def get_dih_criteria():
    return load_yaml("dih_principles.yml")

# Endpoint para indicadores de legitimidad
@router.get("/legitimacy")
def get_legitimacy_indicators():
    return load_yaml("legitimacy_indicators.yml")

# Endpoint combinado (todos los criterios)
@router.get("/all")
def get_all_criteria():
    return {
        "dih_principles": load_yaml("dih_principles.yml"),
        "legitimacy_indicators": load_yaml("legitimacy_indicators.yml")
    }
