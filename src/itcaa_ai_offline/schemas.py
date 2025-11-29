# schemas.py
from pydantic import BaseModel, Field
from typing import List

class PredictionInput(BaseModel):
    features: List[float] = Field(..., description="Liste de valeurs numériques représentant les caractéristiques d’entrée.")

class PredictionOutput(BaseModel):
    label: int = Field(..., description="Classe prédite par le modèle.")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Score de confiance associé à la prédiction.")
