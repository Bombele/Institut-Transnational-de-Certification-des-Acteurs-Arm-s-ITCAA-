from pathlib import Path
import yaml
from db import models

# Ruta base de los diccionarios
DICTIONARIES_PATH = Path("data/dictionaries")

def load_legitimacy_indicators():
    """
    Carga los indicadores de legitimidad desde el archivo YAML.
    """
    file_path = DICTIONARIES_PATH / "legitimacy_indicators.yml"
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["legitimacy_indicators"]

def compute_legitimacy_score(actor: models.Actor) -> float:
    """
    Calcula el score de legitimidad de un actor en base a:
    1. Los indicadores definidos en legitimacy_indicators.yml
    2. Los compromisos (engagements) registrados en la base de datos
    """

    indicators = load_legitimacy_indicators()

    # Base: media de los pesos definidos en el YAML
    base_score = sum(indicators.values()) / len(indicators)

    # Ajuste dinámico según los engagements del actor
    bonus = 0.0
    if actor.engagements:
        for engagement in actor.engagements:
            # Si el compromiso es de categoría "community", añadimos un pequeño bonus
            if engagement.category == "community":
                bonus += 0.05
            # Si es "ethics", añadimos otro bonus
            elif engagement.category == "ethics":
                bonus += 0.05
            # Si es "DIH", reforzamos aún más la legitimidad
            elif engagement.category == "DIH":
                bonus += 0.1

    # Score final con límite máximo de 1.0
    final_score = min(base_score + bonus, 1.0)

    return round(final_score, 2)
from pathlib import Path
import yaml
from db import models

DICTIONARIES_PATH = Path("data/dictionaries")

def load_legitimacy_indicators():
    """
    Charge les indicateurs de légitimité depuis le fichier YAML enrichi.
    """
    file_path = DICTIONARIES_PATH / "legitimacy_indicators.yml"
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)["legitimacy_indicators"]

def compute_legitimacy_score(actor: models.Actor) -> float:
    """
    Calcule le score de légitimité d'un acteur en fonction :
    1. des poids définis dans legitimacy_indicators.yml
    2. des engagements documentés de l'acteur
    """

    indicators = load_legitimacy_indicators()

    # Score de base = moyenne des poids
    base_score = sum(ind["weight"] for ind in indicators.values()) / len(indicators)

    # Bonus dynamique selon les engagements
    bonus = 0.0
    if actor.engagements:
        for engagement in actor.engagements:
            for indicator_name, indicator_data in indicators.items():
                if engagement.category in indicator_data.get("linked_engagements", []):
                    bonus += indicator_data["weight"] * 0.1  # bonus proportionnel

    final_score = min(base_score + bonus, 1.0)
    return round(final_score, 2)
