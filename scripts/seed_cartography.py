# scripts/seed_cartography.py
from datetime import datetime
from apps.api.database import init_db, SessionLocal
from apps.api.models_cartography import Actor, ActorType, Region, ActorStatus, InfluenceZone

def run():
    init_db()
    db = SessionLocal()
    a1 = Actor(name="Al-Shabaab", type=ActorType.GANE, region=Region.AFRICA, status=ActorStatus.ACTIVE, started_at=datetime(2006,1,1), aliases=["AS"], languages=["so","ar"])
    a2 = Actor(name="Wagner Group", type=ActorType.PMC, region=Region.EUROPE, status=ActorStatus.ACTIVE, started_at=datetime(2014,1,1), aliases=["Wagner"], languages=["ru"])
    db.add_all([a1, a2]); db.commit()

    # GeoJSON d'exemple (Somalie)
    zone = InfluenceZone(actor_id=a1.id, country="Somalia", province=None, cross_border=True,
                         geojson={"type":"FeatureCollection","features":[]})
    db.add(zone); db.commit()
    db.close()
    print("✅ Seed cartography inséré.")

if __name__ == "__main__":
    run()
