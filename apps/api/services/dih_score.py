from pathlib import Path
import yaml
from db import models

# Ruta base de los diccionarios
DICTIONARIES_PATH = Path("data/dictionaries")

def load_dih_principles():
    """
    Carga los principios DIH desde el archivo YAML.
    """
    file_path = DICTIONARIES_PATH / "dih_principles.yml"
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["dih_principles"]

def compute_dih_score(actor: models.Actor) -> float:
    """
    Calcula el score DIH de un actor en base a los principios definidos.
    Por ahora, devuelve un promedio simple de los pesos.
    Más adelante se puede enriquecer con evidencias de Engagement.
    """
    principles = load_dih_principles()

    # Ejemplo: si no hay datos específicos del actor, devolvemos la media de los pesos
    score = sum(principles.values()) / len(principles)

    return round(score, 2)
