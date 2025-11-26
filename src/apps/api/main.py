from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# Import des routers (adapte selon ceux que tu as réellement dans src/apps/api/routers)
from apps.api.routers import (
    actors,
    certification,
    capsules,
    criteria,
    geo,
    governance,
    econ,
    reports,
    clients_partners,
    risks,
    cartography,
    cartography_admin,
    observatory,
    ui,
    export,
    health,
)

from apps.api.middleware import AuditMiddleware

# Création de l'application FastAPI
app = FastAPI(
    title="ITCAA API",
    description="Interface institutionnelle pour certification DIH, cartographie et gouvernance citoyenne",
    version="1.0.0"
)

# Middleware d’audit
app.add_middleware(AuditMiddleware)

# Inclusion des routes (ajuste selon les modules que tu as vraiment)
app.include_router(actors.router, prefix="/actors", tags=["Actors"])
app.include_router(certification.router, prefix="/certification", tags=["Certification DIH"])
app.include_router(capsules.router, prefix="/capsules", tags=["Capsules"])
app.include_router(criteria.router, prefix="/criteria", tags=["Criteria"])
app.include_router(geo.router, prefix="/geo", tags=["Cartographie"])
app.include_router(governance.router, prefix="/governance", tags=["Gouvernance"])
app.include_router(econ.router, prefix="/econ", tags=["Économie"])
app.include_router(reports.router, prefix="/reports", tags=["Rapports"])
app.include_router(clients_partners.router, prefix="/clients-partners", tags=["Clients & Partenaires"])
app.include_router(risks.router, prefix="/risks", tags=["Risques"])
app.include_router(cartography.router, prefix="/cartography", tags=["Cartographie"])
app.include_router(cartography_admin.router, prefix="/cartography-admin", tags=["Cartographie Admin"])
app.include_router(observatory.router, prefix="/observatory", tags=["Observatoire"])
app.include_router(ui.router, prefix="/ui", tags=["Interface"])
app.include_router(export.router, prefix="/export", tags=["Export"])
app.include_router(health.router, prefix="/health", tags=["Santé"])

# Endpoint de test
@app.get("/status")
def status_check():
    return {
        "status": "ok",
        "version": "1.0.0",
        "modules": ["apps.api.main", "apps.api.routers"],
        "routes": [route.path for route in app.routes]
    }

# Static files (si tu as un dossier /static)
app.mount("/static", StaticFiles(directory="static"), name="static")
