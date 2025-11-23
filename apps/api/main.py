# apps/api/main.py
from fastapi import FastAPI
from routers import actors, certification, capsules, criteria, geo

app = FastAPI(title="ITCAA API", version="0.1.0")

app.include_router(actors.router, prefix="/actors", tags=["Actors"])
app.include_router(certification.router, prefix="/certification", tags=["Certification"])
app.include_router(capsules.router, prefix="/capsules", tags=["Capsules"])
app.include_router(criteria.router, prefix="/criteria", tags=["Criteria"])
app.include_router(geo.router, prefix="/geo", tags=["Geo"])
