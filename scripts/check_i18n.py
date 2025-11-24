import json
from pathlib import Path

I18N_DIR = Path("data/i18n")
SUPPORTED_LANGS = ["en", "fr", "es", "ar", "ru", "zh"]

def load_translations(lang: str) -> dict:
    path = I18N_DIR / f"{lang}.json"
    if not path.exists():
        raise FileNotFoundError(f"❌ Fichier manquant: {path}")
    return json.loads(path.read_text(encoding="utf-8"))

def check_keys():
    print("🔍 Vérification des fichiers i18n...")
    all_keys = {}
    for lang in SUPPORTED_LANGS:
        translations = load_translations(lang)
        all_keys[lang] = set(translations.keys())

    # Utiliser l'anglais comme référence
    ref_keys = all_keys["en"]
    success = True

    for lang, keys in all_keys.items():
        missing = ref_keys - keys
        extra = keys - ref_keys
        if missing:
            print(f"⚠️ {lang}.json manque {len(missing)} clés: {missing}")
            success = False
        if extra:
            print(f"⚠️ {lang}.json contient {len(extra)} clés en trop: {extra}")
            success = False
        if not missing and not extra:
            print(f"✅ {lang}.json est complet et cohérent.")

    if success:
        print("🎉 Tous les fichiers i18n sont cohérents.")
    else:
        print("❌ Des incohérences ont été détectées.")


if __name__ == "__main__":
    check_keys()
