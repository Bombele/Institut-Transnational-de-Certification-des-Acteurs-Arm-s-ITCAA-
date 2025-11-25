# apps/api/routers/cartography_admin.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.security import require_role
from apps.api.security_models import Role
from apps.api.models_cartography import Actor

router = APIRouter(prefix="/cartography/admin", tags=["cartography-admin"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/actors", dependencies=[Depends(require_role([Role.ADMIN, Role.JURIST]))])
def create_actor_secure(payload: dict, db: Session = Depends(get_db)):
    a = Actor(**payload); db.add(a); db.commit(); db.refresh(a); return a
