# routes.py
from fastapi import APIRouter
from schemas import PredictionInput, PredictionOutput
from predictor import predict

router = APIRouter()

@router.post("/predict", response_model=PredictionOutput)
def get_prediction(input_data: PredictionInput):
    """
    Endpoint REST pour obtenir une prédiction IA hors ligne.
    """
    return predict(input_data)
