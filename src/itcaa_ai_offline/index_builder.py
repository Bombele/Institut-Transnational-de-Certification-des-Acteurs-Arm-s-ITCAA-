from __future__ import annotations
import json
from pathlib import Path
from typing import List, Tuple
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from .config import PATHS, EMBEDDING_MODEL

def read_corpus_files(corpus_dir: Path) -> List[Tuple[str, str]]:
    docs: List[Tuple[str, str]] = []
    for p in sorted(corpus_dir.glob("*.txt")):
        text = p.read_text(encoding="utf-8").strip()
        if text:
            docs.append((p.name, text))
    if not docs:
        raise FileNotFoundError(f"Aucun document trouvé dans {corpus_dir}")
    return docs

def build_embeddings(texts: List[str]) -> np.ndarray:
    model = SentenceTransformer(EMBEDDING_MODEL)
    vectors = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return vectors.astype("float32")

def save_faiss_index(vectors: np.ndarray, meta: List[dict], index_path: Path, meta_path: Path) -> None:
    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)  # Inner Product avec vecteurs normalisés = cosinus
    index.add(vectors)
    index_path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(index_path))
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

def build_index() -> None:
    docs = read_corpus_files(PATHS.corpus_dir)
    texts = [t for _, t in docs]
    vectors = build_embeddings(texts)
    meta = [{"id": i, "filename": fname, "text": text} for i, (fname, text) in enumerate(docs)]
    save_faiss_index(vectors, meta, PATHS.faiss_index, PATHS.meta_json)

if __name__ == "__main__":
    build_index()
    print(f"Index construit: {PATHS.faiss_index}")
