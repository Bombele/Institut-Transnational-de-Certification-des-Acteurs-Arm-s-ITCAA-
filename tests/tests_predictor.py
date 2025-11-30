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

import os
from pathlib import Path
from itcaa_ai_offline.config import PATHS
from itcaa_ai_offline.index_builder import build_index
from itcaa_ai_offline.predictor import OfflinePredictor

def setup_module(module=None):
    # Construit l'index avant les tests si absent
    if (not PATHS.faiss_index.exists()) or (not PATHS.meta_json.exists()):
        build_index()

def test_answer_non_empty():
    predictor = OfflinePredictor()
    ans = predictor.answer("Quels sont les principes du DIH ?")
    assert "Réponse basée sur la base locale" in ans
    assert len(ans.splitlines()) >= 2

def test_empty_query():
    predictor = OfflinePredictor()
    hits = predictor.search("")
    assert hits == []

def test_query_specificity():
    predictor = OfflinePredictor()
    hits = predictor.search("ONU mécanismes")
    assert len(hits) >= 1
    # score doit être entre -1 et 1 (cosinus)
    assert all(-1.0 <= s <= 1.0 for s, _ in hits)

import pytest
from itcaa_ai_offline.predictor import OfflinePredictor
from itcaa_ai_offline.schemas import PredictionInput


def test_semantic_answer():
    """
    Vérifie que le mode semantic retourne une réponse non vide
    quand on interroge le corpus local.
    """
    predictor = OfflinePredictor(mode="semantic")
    result = predictor.answer("Quels sont les principes du DIH ?")
    assert isinstance(result, str)
    assert "Réponse basée sur la base locale" in result or "⚠️" in result


def test_semantic_search():
    """
    Vérifie que la recherche FAISS retourne une liste de tuples (score, meta).
    """
    predictor = OfflinePredictor(mode="semantic")
    results = predictor.search("humanitaire", k=3)
    assert isinstance(results, list)
    if results:  # si corpus non vide
        score, meta = results[0]
        assert isinstance(score, float)
        assert isinstance(meta, dict)


def test_classifier_predict():
    """
    Vérifie que le mode classifier retourne un PredictionOutput
    avec label et confiance.
    """
    predictor = OfflinePredictor(mode="classifier")
    dummy_input = PredictionInput(features=[0.1, 0.2, 0.3])  # exemple simple
    output = predictor.predict(dummy_input)
    assert hasattr(output, "label")
    assert hasattr(output, "confidence")
    assert isinstance(output.label, int)
    assert isinstance(output.confidence, float)
    assert 0.0 <= output.confidence <= 1.0
