import json
from sqlalchemy.orm import Session
from apps.api.db.session import SessionLocal
from apps.api.db import models

def export_actors_to_geojson(output_path="data/geo/actors.geojson"):
    """
    Exporte tous les acteurs de la base en format GeoJSON.
    Chaque acteur est représenté comme une Feature avec ses propriétés et sa géométrie.
    """
    db: Session = SessionLocal()
    actors = db.query(models.Actor).all()

    features = []
    for actor in actors:
        # Chaque acteur doit avoir un champ geojson (Point ou Polygon)
        geometry = actor.geojson if actor.geojson else None

        feature = {
            "type": "Feature",
            "properties": {
                "id": actor.id,
                "name": actor.name,
                "acronym": actor.acronym,
                "typology": actor.typology,
                "country": actor.country,
                "region": actor.region
            },
            "geometry": geometry
        }
        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(geojson, f, ensure_ascii=False, indent=2)

    print(f"✅ Export terminé : {output_path}")


if __name__ == "__main__":
    export_actors_to_geojson()
