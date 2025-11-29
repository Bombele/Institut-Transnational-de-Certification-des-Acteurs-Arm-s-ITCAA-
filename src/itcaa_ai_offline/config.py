from pathlib import Path
from dataclasses import dataclass

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CORPUS_DIR = DATA_DIR / "corpus"
INDEX_DIR = DATA_DIR / "index"

@dataclass(frozen=True)
class Paths:
    corpus_dir: Path = CORPUS_DIR
    index_dir: Path = INDEX_DIR
    faiss_index: Path = INDEX_DIR / "faiss.index"
    meta_json: Path = INDEX_DIR / "meta.json"

PATHS = Paths()
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # léger et rapide
TOP_K = 3
