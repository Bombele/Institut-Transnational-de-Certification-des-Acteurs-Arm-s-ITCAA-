# apps/api/validators.py
def advisory_geobalance(members) -> bool:
    seen = {m.region for m in members if m.active}
    return len(seen) >= 4  # au moins 4 régions représentées
