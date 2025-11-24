# scripts/seed_portfolio.py
from datetime import datetime
from apps.api.database import init_db, SessionLocal
from apps.api.models_actors import Actor, ActorType, Region, Client, Partner

def run():
    init_db()
    db = SessionLocal()
    actors = [
        Actor(name="FARC dissidents", type=ActorType.GANE, region=Region.AMERICAS, started_at=datetime(2017,1,1)),
        Actor(name="Al-Shabaab", type=ActorType.GANE, region=Region.AFRICA, started_at=datetime(2006,1,1)),
        Actor(name="Houthis", type=ActorType.HYBRID, region=Region.MENA, started_at=datetime(2004,1,1)),
        Actor(name="Wagner Group", type=ActorType.PMC, region=Region.EUROPE, started_at=datetime(2014,1,1)),
        Actor(name="G4S", type=ActorType.PMC, region=Region.GLOBAL, started_at=datetime(1990,1,1)),
    ]
    clients = [
        Client(name="ONU", category="UN", country="GLOBAL"),
        Client(name="CICR", category="NGO", country="GLOBAL")
    ]
    partners = [
        Partner(name="Geneva Academy", type="UNIVERSITY"),
        Partner(name="GRIP", type="THINKTANK")
    ]
    db.add_all(actors + clients + partners)
    db.commit(); db.close()
    print("✅ Seed portfolio inséré.")

if __name__ == "__main__":
    run()
