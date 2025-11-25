# apps/api/econ_service.py
import yaml
from pathlib import Path
from sqlalchemy.orm import Session
from apps.api.econ_models import Revenue, Cost

def load_econ_config():
    data = yaml.safe_load(Path("econ/config.yml").read_text(encoding="utf-8"))
    return data

def annual_totals(db: Session) -> dict:
    rev = sum(r.amount for r in db.query(Revenue).all())
    cost = sum(c.amount for c in db.query(Cost).all())
    return {"total_revenue": rev, "total_costs": cost, "net": rev - cost}

def simulate_baseline() -> dict:
    cfg = load_econ_config()
    rb = cfg["revenue_bands"]; cb = cfg["cost_baselines"]; A = cfg["assumptions"]

    revenue = (
        rb["certification"][1] * A["certifications_per_year"] +
        rb["training_per_person"][1] * A["trainings_people_per_year"] +
        rb["consulting_contracts"][1] * A["consulting_contracts_per_year"] +
        rb["licenses_per_year"][1] * A["licenses_per_year"] +
        rb["grants_per_year"][1]
    )

    costs = (
        cb["maintenance_annual"] +
        cb["multilingual_per_language_annual"] * A["languages_onu"] +
        cb["team_annual"] +
        cb["diplomacy_annual"] +
        cb["communication_annual"]
    )

    net = revenue - costs
    return {"scenario": "baseline", "revenue": revenue, "costs": costs, "net": net}

def simulate_optimistic() -> dict:
    cfg = load_econ_config()
    rb = cfg["revenue_bands"]; cb = cfg["cost_baselines"]; A = cfg["assumptions"]
    revenue = (
        rb["certification"][2] * (A["certifications_per_year"] + 5) +
        rb["training_per_person"][2] * (A["trainings_people_per_year"] + 100) +
        rb["consulting_contracts"][2] * (A["consulting_contracts_per_year"] + 2) +
        rb["licenses_per_year"][2] * (A["licenses_per_year"] + 10) +
        rb["grants_per_year"][2]
    )
    costs = (
        cb["maintenance_annual"] +
        cb["multilingual_per_language_annual"] * A["languages_onu"] +
        cb["team_annual"] * 1.2 +
        cb["diplomacy_annual"] * 1.3 +
        cb["communication_annual"] * 1.2
    )
    return {"scenario": "optimistic", "revenue": revenue, "costs": costs, "net": revenue - costs}

def simulate_conservative() -> dict:
    cfg = load_econ_config()
    rb = cfg["revenue_bands"]; cb = cfg["cost_baselines"]; A = cfg["assumptions"]
    revenue = (
        rb["certification"][0] * max(A["certifications_per_year"] - 5, 3) +
        rb["training_per_person"][0] * max(A["trainings_people_per_year"] - 100, 50) +
        rb["consulting_contracts"][0] * max(A["consulting_contracts_per_year"] - 2, 1) +
        rb["licenses_per_year"][0] * max(A["licenses_per_year"] - 5, 3) +
        rb["grants_per_year"][0]
    )
    costs = (
        cb["maintenance_annual"] +
        cb["multilingual_per_language_annual"] * A["languages_onu"] +
        cb["team_annual"] * 0.9 +
        cb["diplomacy_annual"] * 0.8 +
        cb["communication_annual"] * 0.9
    )
    return {"scenario": "conservative", "revenue": revenue, "costs": costs, "net": revenue - costs}
