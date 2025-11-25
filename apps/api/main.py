# apps/api/main.py
from fastapi import FastAPI
from routers import actors, certification, capsules, criteria, geo

app = FastAPI(title="ITCAA API", version="0.1.0")

app.include_router(actors.router, prefix="/actors", tags=["Actors"])
app.include_router(certification.router, prefix="/certification", tags=["Certification"])
app.include_router(capsules.router, prefix="/capsules", tags=["Capsules"])
app.include_router(criteria.router, prefix="/criteria", tags=["Criteria"])
app.include_router(geo.router, prefix="/geo", tags=["Geo"])
from fastapi import FastAPI
from apps.api.routers import certification, econ, reports

app = FastAPI(title="ITCAA API")

# Brancher les routes
app.include_router(certification.router)
app.include_router(econ.router)
app.include_router(reports.router)
# apps/api/main.py
from fastapi import FastAPI
from apps.api.routers import certification, actors, clients_partners, risks, econ, reports

app = FastAPI(title="ITCAA API")
app.include_router(certification.router)
app.include_router(actors.router)
app.include_router(clients_partners.router)
app.include_router(risks.router)
app.include_router(econ.router)
app.include_router(reports.router)
# apps/api/main.py
from fastapi import FastAPI
from apps.api.middleware import AuditMiddleware
from apps.api.routers import certification, governance
from apps.api.routers import econ, reports, actors, clients_partners, risks

app = FastAPI(title="ITCAA API")

# Middleware d’audit (journalisation de chaque requête)
app.add_middleware(AuditMiddleware)

# Routes
app.include_router(certification.router)
app.include_router(governance.router)
app.include_router(econ.router)
app.include_router(reports.router)
app.include_router(actors.router)
app.include_router(clients_partners.router)
app.include_router(risks.router)
# apps/api/main.py
from fastapi import FastAPI
from apps.api.routers import cartography, cartography_admin, observatory, reports

app = FastAPI(title="ITCAA API")
app.include_router(cartography.router)
app.include_router(cartography_admin.router)
app.include_router(observatory.router)
app.include_router(reports.router)
# apps/api/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from apps.api.routers import ui, cartography, export, reports

app = FastAPI(title="ITCAA")
app.include_router(ui.router)
app.include_router(cartography.router)
app.include_router(export.router)
app.include_router(reports.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
from apps.api.routers import health, actors, certification, capsules, criteria, geo
