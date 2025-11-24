# scripts/seed_econ.py
from datetime import datetime
from apps.api.database import SessionLocal, init_db
from apps.api.econ_models import Revenue, Cost, RevenueType, CostType

def run():
    init_db()
    db = SessionLocal()
    # Revenus
    db.add_all([
        Revenue(type=RevenueType.CERTIFICATION, title="Certifications 10/an", amount=300000, org_name="ITCAA", recorded_at=datetime.utcnow()),
        Revenue(type=RevenueType.TRAINING, title="Formations 200 personnes", amount=200000, org_name="ITCAA", recorded_at=datetime.utcnow()),
        Revenue(type=RevenueType.CONSULTING, title="Consulting 3 contrats", amount=450000, org_name="ITCAA", recorded_at=datetime.utcnow()),
        Revenue(type=RevenueType.PUBLICATION, title="Licences & publications", amount=100000, org_name="ITCAA", recorded_at=datetime.utcnow()),
        Revenue(type=RevenueType.GRANT, title="Subventions", amount=500000, org_name="Donors", recorded_at=datetime.utcnow()),
    ])
    # Coûts
    db.add_all([
        Cost(type=CostType.MAINTENANCE, title="Maintenance annuelle", amount=150000, recorded_at=datetime.utcnow()),
        Cost(type=CostType.MULTILINGUAL, title="Multilinguisme 6 langues", amount=100000, recorded_at=datetime.utcnow()),
        Cost(type=CostType.TEAM, title="Équipe de base", amount=400000, recorded_at=datetime.utcnow()),
        Cost(type=CostType.DIPLOMACY, title="Diplomatie & forums", amount=100000, recorded_at=datetime.utcnow()),
        Cost(type=CostType.COMMUNICATION, title="Communication & mémoire", amount=50000, recorded_at=datetime.utcnow()),
    ])
    db.commit(); db.close()
    print("✅ Seed économique ITCAA inséré.")

if __name__ == "__main__":
    run()
python scripts/seed_econ.py
