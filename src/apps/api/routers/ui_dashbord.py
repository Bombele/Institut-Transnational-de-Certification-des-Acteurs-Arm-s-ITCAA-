# apps/api/routers/ui_dashboard.py
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from apps.api.database import SessionLocal
from apps.api.services.tracking_service import check_expiring_mous, check_expiring_mandates

router = APIRouter(prefix="/ui", tags=["ui"])
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    mous = check_expiring_mous(db)
    mandates = check_expiring_mandates(db)
    alerts = []
    for m in mous:
        alerts.append(f"MoU avec {m.partner_name} expire le {m.expires_at}")
    for md in mandates:
        alerts.append(f"Mandat du membre {md.member_id} expire le {md.end_date}")
    return templates.TemplateResponse("dashboard.html", {"request": request, "alerts": alerts})
