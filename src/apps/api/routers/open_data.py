# apps/api/routers/open_data.py
@router.get("/datasets")
def list_open_datasets():
    # catalogues: protocols versions, annual reports, geojson layers, anonymized capsules
    ...

# apps/api/routers/audit.py
@router.get("/audit/logs")
def audit_logs(limit: int = 100):
    # évènements: ajout preuve, changement seuil, nouvelle reconnaissance
    ...
