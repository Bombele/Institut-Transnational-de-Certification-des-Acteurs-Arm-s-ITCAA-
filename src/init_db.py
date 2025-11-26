from apps.api.database import init_db, SessionLocal
from apps.api.models.models_actors import Actor, ActorType, Region, Client, ClientCategory, Partner, PartnerType

def seed_data():
    db = SessionLocal()

    # Exemple d’acteurs
    actors = [
        Actor(name="Alpha PMC", type=ActorType.PMC, region=Region.AFRICA),
        Actor(name="Militia Verde", type=ActorType.MILITIA, region=Region.AMERICAS),
        Actor(name="Hybrid Force", type=ActorType.HYBRID, region=Region.ASIA),
    ]

    # Exemple de clients
    clients = [
        Client(name="ONU", category=ClientCategory.UN, country="Global"),
        Client(name="Union Africaine", category=ClientCategory.UA, country="Africa"),
        Client(name="ONG Human Rights Watch", category=ClientCategory.NGO, country="Global"),
    ]

    # Exemple de partenaires
    partners = [
        Partner(name="Université de Bruxelles", type=PartnerType.UNIVERSITY, region=Region.EUROPE),
        Partner(name="ThinkTank Global Policy", type=PartnerType.THINKTANK, region=Region.GLOBAL),
    ]

    # Ajout en base
    db.add_all(actors + clients + partners)
    db.commit()

    print("✅ Données initiales insérées avec succès")

if __name__ == "__main__":
    print("🔧 Initialisation de la base ITCAA...")
    init_db()
    seed_data()
    print("🚀 Base ITCAA prête avec données de test")
