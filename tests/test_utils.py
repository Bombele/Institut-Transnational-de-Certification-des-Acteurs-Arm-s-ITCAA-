# tests/test_utils.py
import pytest
from itcaa_ai_offline.utils import normalize_features, log_prediction
from itcaa_ai_offline.schemas import PredictionInput, PredictionOutput

def test_normalize_features_basic():
    """
    Vérifie que la normalisation transforme les valeurs entre 0 et 1.
    """
    features = [10, 20, 30]
    normalized = normalize_features(features)
    assert normalized == [0.0, 0.5, 1.0], f"Résultat inattendu : {normalized}"

def test_normalize_features_identical_values():
    """
    Vérifie que des valeurs identiques sont normalisées à 0.0.
    """
    features = [5, 5, 5]
    normalized = normalize_features(features)
    assert normalized == [0.0, 0.0, 0.0], f"Résultat inattendu : {normalized}"

def test_log_prediction_creates_log(tmp_path, monkeypatch):
    """
    Vérifie que log_prediction écrit bien dans le fichier LOG_FILE.
    """
    log_file = tmp_path / "ai_offline.log"
    monkeypatch.setenv("LOG_FILE", str(log_file))

    input_data = PredictionInput(features=[0.1, 0.2, 0.3])
    output_data = PredictionOutput(prediction="A", confidence=0.85)

    log_prediction(input_data, output_data)

    assert log_file.exists(), "Le fichier de log n'a pas été créé"
    content = log_file.read_text()
    assert "Input=" in content, "Le log ne contient pas l'entrée"
    assert "Confidence=" in content, "Le log ne contient pas le score de confiance"
