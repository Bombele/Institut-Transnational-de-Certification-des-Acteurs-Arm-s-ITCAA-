from fastapi import APIRouter, HTTPException
import json
from pathlib import Path

router = APIRouter()

# Ruta base de los archivos geo
GEO_PATH = Path("data/geo")

def load_geojson(file_name: str):
    file_path = GEO_PATH / file_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"Archivo {file_name} no encontrado")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Endpoint para países
@router.get("/countries")
def get_countries():
    return load_geojson("countries.geojson")

# Endpoint para regiones
@router.get("/regions")
def get_regions():
    return load_geojson("regions.geojson")

# Endpoint combinado
@router.get("/all")
def get_all_geo():
    return {
        "countries": load_geojson("countries.geojson"),
        "regions": load_geojson("regions.geojson")
    }
