# model_loader.py
import torch
import os

MODEL_PATH = os.path.join("models", "model.pt")

def load_model(path: str = MODEL_PATH):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Modèle introuvable à l’emplacement : {path}")
    model = torch.load(path, map_location=torch.device("cpu"))
    model.eval()
    return model
