from db import models

def classify_actor(actor: models.Actor) -> str:
    """
    Détermine la typologie d'un acteur en fonction de ses attributs.
    Typologies possibles :
      - SMP (Société Militaire Privée)
      - GANE (Groupe Armé Non Étatique)
      - HYBRID (mixte)
    """

    # Exemple de règles simples (à enrichir selon ton modèle institutionnel ITCAA)
    if actor.acronym and "SARL" in actor.acronym.upper():
        return "SMP"
    elif actor.country and actor.country in ["RDC", "Venezuela", "Syrie"]:
        return "GANE"
    elif actor.engagements and any(e.category == "community" for e in actor.engagements):
        return "HYBRID"
    else:
        return "GANE"  # valeur par défaut

def update_actor_typology(db, actor: models.Actor):
    """
    Met à jour la typologie d'un acteur dans la base.
    """
    typology = classify_actor(actor)
    actor.typology = typology
    db.add(actor)
    db.commit()
    db.refresh(actor)
    return actor
