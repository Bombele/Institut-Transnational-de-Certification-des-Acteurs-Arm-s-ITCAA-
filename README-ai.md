# 🧠 Module IA hors ligne – ITCAA

## 🇫🇷 Français

Ce module implémente un système d’intelligence artificielle autonome, conçu pour fonctionner hors ligne. Il renforce la souveraineté technique et la résilience institutionnelle du projet ITCAA.

### Fonctionnalités
- Chargement local du modèle (`model.pt`)
- Prédiction via FastAPI (`/predict`)
- Validation Pydantic des entrées/sorties
- CI/CD local via `offline-ai.yml`

### Usage
```bash
uvicorn main_ai:app --reload
