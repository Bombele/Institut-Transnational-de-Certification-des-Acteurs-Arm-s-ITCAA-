import os
import sys
import yaml
import importlib.util

EXPECTED_COMMAND = "PYTHONPATH=src python -m uvicorn apps.api.main:app --host 0.0.0.0 --port $PORT"

def check_render_yaml():
    path = "render.yaml"
    if not os.path.isfile(path):
        print("❌ Fichier render.yaml introuvable")
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        cmd = data.get("startCommand", "").strip()
        if cmd == EXPECTED_COMMAND:
            print("✅ startCommand correct dans render.yaml")
            return True
        else:
            print("❌ startCommand incorrect")
            print(f"➡️ Actuel : {cmd}")
            print(f"➡️ Attendu : {EXPECTED_COMMAND}")
            return False
    except Exception as e:
        print(f"❌ Erreur de lecture render.yaml : {e}")
        return False

def check_apps_importable():
    try:
        spec = importlib.util.find_spec("apps")
        if spec is not None:
            print("✅ Module 'apps' accessible via PYTHONPATH=src")
            return True
        else:
            print("❌ Module 'apps' introuvable")
            return False
    except Exception as e:
        print(f"❌ Erreur d'import 'apps' : {e}")
        return False

def main():
    print("🔍 Prévalidation du déploiement ITCAA\n")
    os.environ["PYTHONPATH"] = "src"

    ok_yaml = check_render_yaml()
    ok_apps = check_apps_importable()

    if not (ok_yaml and ok_apps):
        print("\n❌ Blocage du déploiement : configuration invalide")
        sys.exit(1)
