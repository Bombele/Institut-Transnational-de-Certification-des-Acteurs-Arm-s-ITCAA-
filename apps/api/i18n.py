import json
from pathlib import Path
from fastapi import Request

# Langues supportées (6 officielles ONU)
SUPPORTED_LANGS = {"en", "fr", "es", "ar", "ru", "zh"}

# Cache pour éviter de recharger les fichiers à chaque requête
_locale_cache = {}


def load_locale(lang: str) -> dict:
    """
    Charge le fichier JSON correspondant à la langue demandée.
    Si la langue n'est pas supportée, on revient à l'anglais.
    """
    if lang not in SUPPORTED_LANGS:
        lang = "en"

    if lang in _locale_cache:
        return _locale_cache[lang]

    path = Path("data/i18n") / f"{lang}.json"
    if not path.exists():
        # fallback anglais si fichier manquant
        path = Path("data/i18n/en.json")

    with open(path, "r", encoding="utf-8") as f:
        translations = json.load(f)

    _locale_cache[lang] = translations
    return translations


def get_lang(request: Request) -> str:
    """
    Détecte la langue depuis :
    1. Paramètre de requête ?lang=xx
    2. Header Accept-Language
    3. Fallback anglais
    """
    # Query param prioritaire
    q = request.query_params.get("lang")
    if q in SUPPORTED_LANGS:
        return q

    # Header Accept-Language
    hdr = request.headers.get("Accept-Language", "")
    for part in hdr.split(","):
        code = part.strip().split(";")[0].split("-")[0]
        if code in SUPPORTED_LANGS:
            return code

    return "en"
# apps/api/i18n.py
import json
from pathlib import Path

def load_locale(lang: str):
    path = Path(f"data/i18n/{lang}.json")
    if not path.exists():
        path = Path("data/i18n/en.json")  # fallback
    return json.loads(path.read_text(encoding="utf-8"))

def get_lang(request):
    return request.query_params.get("lang") or "en"
