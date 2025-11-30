#!/bin/bash
# Reconstruit l'index FAISS automatiquement si de nouveaux fichiers apparaissent

set -euo pipefail  # Sécurité : stoppe en cas d'erreur ou variable non définie

CORPUS_DIR="src/itcaa_ai_offline/data/corpus"
INDEX_FILE="src/itcaa_ai_offline/data/index/faiss.index"

echo "🔍 Vérification des nouveaux fichiers dans $CORPUS_DIR..."

# Vérifie que le dossier corpus existe
if [ ! -d "$CORPUS_DIR" ]; then
  echo "❌ Dossier corpus introuvable: $CORPUS_DIR"
  exit 1
fi

# Vérifie si l'index existe déjà
if [ ! -f "$INDEX_FILE" ]; then
  echo "⚙️ Aucun index trouvé, construction initiale..."
  python -m itcaa_ai_offline.index_builder
else
  # Compare les dates de modification
  NEWER=$(find "$CORPUS_DIR" -type f -newer "$INDEX_FILE" || true)
  if [ -n "$NEWER" ]; then
    echo "⚙️ Nouveaux fichiers détectés, reconstruction de l'index..."
    python -m itcaa_ai_offline.index_builder
  else
    echo "✅ Index déjà à jour."
  fi
fi
