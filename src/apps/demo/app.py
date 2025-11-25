from fastapi import FastAPI
from apps.api.routers import actors, capsules, certification, criteria, geo

# Créer l'application FastAPI
app = FastAPI(
    title="Justice Digital Demo",
    description="Démo ITCAA – Certification et typologie des acteurs armés",
    version="1.0.0"
)

# Inclure les routers principaux
app.include_router(actors.router, prefix="/actors", tags=["Actors"])
app.include_router(capsules.router, prefix="/capsules", tags=["Capsules"])
app.include_router(certification.router, prefix="/certification", tags=["Certification"])
app.include_router(criteria.router, prefix="/criteria", tags=["Criteria"])
app.include_router(geo.router, prefix="/geo", tags=["Geo"])

# Endpoint de bienvenue
@app.get("/")
def root():
    return {
        "message": "Bienvenue dans la démo ITCAA 🚀",
        "routers": [
            "/actors",
            "/capsules",
            "/certification",
            "/criteria",
            "/geo"
        ]
    }
