# predictor.py
from model_loader import load_model
from schemas import PredictionInput, PredictionOutput
from utils import normalize_features, log_prediction
import torch

# Charger le modèle IA hors ligne
model = load_model()

def predict(input_data: PredictionInput) -> PredictionOutput:
    # 🧹 Normalisation des données d’entrée
    normalized_features = normalize_features(input_data.features)

    # Conversion en tenseur
    input_tensor = torch.tensor([normalized_features], dtype=torch.float32)

    # Prédiction
    with torch.no_grad():
        output = model(input_tensor)

    # Traitement du résultat
    prediction = output.argmax(dim=1).item()
    confidence = torch.nn.functional.softmax(output, dim=1)[0][prediction].item()

    # 📝 Journalisation pour auditabilité
    log_prediction(input_data.features, prediction, confidence)

    return PredictionOutput(
        label=prediction,
        confidence=round(confidence, 4)
    )
