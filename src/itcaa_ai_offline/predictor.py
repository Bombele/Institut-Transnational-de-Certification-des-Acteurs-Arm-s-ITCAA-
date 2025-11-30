from __future__ import annotations
import json
from typing import List, Tuple
import numpy as np
import faiss
import torch
from sentence_transformers import SentenceTransformer
from .config import PATHS, EMBEDDING_MODEL, TOP_K
from .modelloader import load_model
from .schemas import PredictionInput, PredictionOutput
from .utils import normalize_features, log_prediction


class OfflinePredictor:
    """
    IA hors ligne hybride : recherche sémantique (FAISS) ou classification supervisée (Torch).
    """

    def __init__(self, mode: str = "semantic") -> None:
        self.mode = mode
        if self.mode == "semantic":
            self._init_semantic()
        elif self.mode == "classifier":
            self._init_classifier()
        else:
            raise ValueError(f"Mode inconnu: {self.mode}")

    def _init_semantic(self) -> None:
        if not PATHS.faiss_index.exists():
            raise FileNotFoundError(f"Index FAISS introuvable: {PATHS.faiss_index}")
        if not PATHS.meta_json.exists():
            raise FileNotFoundError(f"Métadonnées introuvables: {PATHS.meta_json}")

        self.index = faiss.read_index(str(PATHS.faiss_index))
        self.meta = json.loads(PATHS.meta_json.read_text(encoding="utf-8"))
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def _init_classifier(self) -> None:
        self.model = load_model()

    def search(self, query: str, k: int = TOP_K) -> List[Tuple[float, dict]]:
        if not query.strip():
            return []

        q_vec = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        scores, ids = self.index.search(q_vec, k)
        results: List[Tuple[float, dict]] = []

        for score, idx in zip(scores[0].tolist(), ids[0].tolist()):
            if idx == -1 or idx >= len(self.meta):
                continue
            results.append((float(score), self.meta[idx]))

        return results

    def answer(self, query: str, k: int = TOP_K) -> str:
        hits = self.search(query, k=k)
        if not hits:
            return "⚠️ Aucune information disponible dans la base locale."
        parts = [f"- {m['text']}" for _, m in hits]
        return "Réponse basée sur la base locale:\n" + "\n".join(parts)

    def predict(self, input_data: PredictionInput) -> PredictionOutput:
        features = normalize_features(input_data.features)
        input_tensor = torch.tensor([features], dtype=torch.float32)

        with torch.no_grad():
            output = self.model(input_tensor)

        prediction = output.argmax(dim=1).item()
        confidence = torch.nn.functional.softmax(output, dim=1)[0][prediction].item()

        log_prediction(input_data.features, prediction, confidence)

        return PredictionOutput(
            label=prediction,
            confidence=round(confidence, 4)
        )


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m itcaa_ai_offline.predictor \"votre question\"")
        raise SystemExit(1)

    query = " ".join(sys.argv[1:])
    predictor = OfflinePredictor(mode="semantic")
    print(predictor.answer(query))
