from typing import Dict, Any

def format_actor(actor: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formate un acteur pour l'affichage dans la démo.
    """
    return {
        "id": actor.get("id"),
        "name": actor.get("name"),
        "acronym": actor.get("acronym"),
        "typology": actor.get("typology"),
        "country": actor.get("country"),
        "region": actor.get("region"),
    }

def format_capsule(capsule: Dict[str, Any]) -> Dict[str, Any]:
    """
    Formate une capsule pour l'affichage.
    """
    return {
        "id": capsule.get("id"),
        "actor_id": capsule.get("actor_id"),
        "narrative": capsule.get("narrative"),
        "scores": {
            "legitimacy": capsule.get("legitimacy_score"),
            "dih": capsule.get("dih_score"),
            "certification": capsule.get("certification_score"),
        },
        "version": capsule.get("version"),
        "validations": capsule.get("validations"),
    }

def summary_certification(actor_name: str, dih: float, legitimacy: float, certification: float) -> str:
    """
    Génère un résumé narratif de la certification.
    """
    return (
        f"Acteur {actor_name} : score DIH = {dih}, "
        f"score légitimité = {legitimacy}, "
        f"score certification final = {certification}."
    )

def api_overview() -> Dict[str, Any]:
    """
    Retourne une vue d'ensemble des composants disponibles dans la démo.
    """
    return {
        "components": [
            "format_actor",
            "format_capsule",
            "summary_certification",
            "api_overview"
        ],
        "description": "Composants réutilisables pour la démo ITCAA"
  }
