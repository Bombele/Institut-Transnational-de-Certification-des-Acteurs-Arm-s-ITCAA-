#!/bin/bash

echo "🔧 Installation des dépendances..."
pip install -r requirements.txt

echo "🧠 Configuration du PYTHONPATH..."
export PYTHONPATH=src

echo "🚀 Lancement de l'API ITCAA..."
uvicorn apps.api.main:app --host 0.0.0.0 --port 8000 --reload
