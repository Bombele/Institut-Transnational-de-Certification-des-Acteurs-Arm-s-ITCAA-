# apps/api/routers/econ.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from apps.api.database import SessionLocal
from apps.api.econ_models import Revenue, Cost, EconContract, EconProjection
from apps.api.econ_service import annual_totals, simulate_baseline, simulate_optimistic, simulate_conservative

router = APIRouter(prefix="/econ", tags=["economics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/totals")
def get_totals(db: Session = Depends(get_db)):
    return annual_totals(db)

@router.get("/simulate")
def simulate(scenario: str = "baseline"):
    if scenario == "optimistic":
        return simulate_optimistic()
    if scenario == "conservative":
        return simulate_conservative()
    return simulate_baseline()

@router.get("/revenues")
def list_revenues(db: Session = Depends(get_db)):
    return db.query(Revenue).all()

@router.post("/revenues")
def add_revenue(payload: dict, db: Session = Depends(get_db)):
    r = Revenue(**payload)
    db.add(r); db.commit(); db.refresh(r)
    return r

@router.get("/costs")
def list_costs(db: Session = Depends(get_db)):
    return db.query(Cost).all()

@router.post("/costs")
def add_cost(payload: dict, db: Session = Depends(get_db)):
    c = Cost(**payload)
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.get("/contracts")
def list_contracts(db: Session = Depends(get_db)):
    return db.query(EconContract).all()

@router.post("/contracts")
def add_contract(payload: dict, db: Session = Depends(get_db)):
    ct = EconContract(**payload)
    db.add(ct); db.commit(); db.refresh(ct)
    return ct

@router.get("/projections")
def list_projections(db: Session = Depends(get_db)):
    return db.query(EconProjection).all()

@router.post("/projections")
def add_projection(payload: dict, db: Session = Depends(get_db)):
    pr = EconProjection(**payload)
    db.add(pr); db.commit(); db.refresh(pr)
    return pr
