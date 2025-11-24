# ITCAA – Déploiement sur Hugging Face Spaces

## 🎯 Objectif
Ce document décrit la procédure pour déployer l’application **ITCAA** sur [Hugging Face Spaces](https://huggingface.co/spaces).  
Spaces permet de partager des applications interactives basées sur **Gradio** ou **FastAPI**, avec une intégration transparente des modèles IA et des APIs.

---

## 🏗️ Prérequis

- Compte Hugging Face
- Repository GitHub ou code source local
- Fichier `requirements.txt` listant les dépendances :
  ```txt
  fastapi
  uvicorn
  sqlalchemy
  shapely
  pyyaml
