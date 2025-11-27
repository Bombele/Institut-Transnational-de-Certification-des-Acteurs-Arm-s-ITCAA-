# utils.py
import logging
import datetime
from typing import List

# 📌 Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/ai_offline.log"),  # Sauvegarde dans un fichier
        logging.StreamHandler()                      # Affichage console
    ]
)

logger = logging.getLogger("ITCAA_AI_Offline")


# 🧹 Prétraitement des données
def normalize_features(features: List[float]) -> List[float]:
    """
    Normalise une liste de valeurs numériques entre 0 et 1.
    """
    if not features:
        raise ValueError("La liste des features est vide.")
    min_val, max_val = min(features), max(features)
    if min_val == max_val:
        return [0.0 for _ in features]
    return [(f - min_val) / (max_val - min_val) for f in features]


# 📝 Auditabilité : journalisation des prédictions
def log_prediction(input_data: List[float], label: int, confidence: float):
    """
    Enregistre une prédiction dans les logs avec horodatage.
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    logger.info(
        f"[{timestamp}] Input={input_data} → Label={label}, Confidence={confidence:.4f}"
  )
