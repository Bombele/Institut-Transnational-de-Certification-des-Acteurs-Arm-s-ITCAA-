from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import des routers
from apps.api.routers import actors, clients, partners, risk_register

# 📌 Création de l’application FastAPI
app = FastAPI(
    title="ITCAA – Institut Transnational de Certification des Acteurs Armés",
    description="""
    🌍 ITCAA est une initiative citoyenne et institutionnelle visant à certifier les acteurs armés non étatiques
    selon leur conformité au Droit International Humanitaire (DIH), leur légitimité institutionnelle et leurs normes internes.
    
    Cette API fournit des endpoints pour gérer :
    - 🎭 Acteurs
    - 🏛️ Clients
    - 🤝 Partenaires
    - ⚠️ Registre des risques
    
    Documentation générée automatiquement pour auditabilité et transparence.
    """,
    version="1.0.0",
    contact={
        "name": "Camille Bombele Liyama",
        "email": "contact@itcaa.org",
        "url": "https://github.com/Bombele/ITCAA"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# 🔓 Configuration CORS
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://itcaa.org",
    "https://*.itcaa.org"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Autoriser les domaines front-end
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 Inclusion des routers
app.include_router(actors.router)
app.include_router(clients.router)
app.include_router(partners.router)
app.include_router(risk_register.router)

# 🏠 Endpoint racine
@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Bienvenue sur l’API ITCAA 🌍 – Certification citoyenne et institutionnelle",
        "docs": "/docs",
        "redoc": "/redoc"
}
