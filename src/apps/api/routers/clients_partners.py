# apps/api/routers/clients_partners.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.models_actors import Client, Partner, ActorClientLink, ActorPartnerLink

router = APIRouter(prefix="/relations", tags=["relations"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/clients")
def list_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@router.post("/clients")
def add_client(payload: dict, db: Session = Depends(get_db)):
    c = Client(**payload); db.add(c); db.commit(); db.refresh(c); return c

@router.get("/partners")
def list_partners(db: Session = Depends(get_db)):
    return db.query(Partner).all()

@router.post("/partners")
def add_partner(payload: dict, db: Session = Depends(get_db)):
    p = Partner(**payload); db.add(p); db.commit(); db.refresh(p); return p

@router.post("/link/actor-client")
def link_actor_client(payload: dict, db: Session = Depends(get_db)):
    link = ActorClientLink(**payload); db.add(link); db.commit(); db.refresh(link); return link

@router.post("/link/actor-partner")
def link_actor_partner(payload: dict, db: Session = Depends(get_db)):
    link = ActorPartnerLink(**payload); db.add(link); db.commit(); db.refresh(link); return link
