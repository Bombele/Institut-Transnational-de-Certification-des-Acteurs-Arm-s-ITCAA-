# ITCAA – Architecture Technique

## 🎯 Objectif
L’Institut Transnational de Certification des Acteurs Armés (ITCAA) fournit une plateforme de **justice digitale** permettant :
- La certification des acteurs armés non étatiques.
- L’évaluation de leur conformité au **DIH** (Droit International Humanitaire).
- La mesure de leur **légitimité institutionnelle** et de leurs **normes internes**.
- La documentation narrative et comparative pour la diaspora et les institutions.

---

## 🏗️ Structure générale
---

## ⚙️ Composants principaux

### 1. **Base de données (`apps/api/db`)**
- **`models.py`** : définit `Actor`, `Engagement`, `Capsule`, `Criterion`.
- **`session.py`** : gestion des connexions DB.
- **`base.py`** : métadonnées SQLAlchemy.

### 2. **Routers (`apps/api/routers`)**
- `actors.py` → CRUD des acteurs.
- `capsules.py` → gestion des capsules de certification.
- `certification.py` → calcul des scores DIH, légitimité, normes internes.
- `criteria.py` → exposition des critères YAML.
- `geo.py` → endpoints géospatiaux (acteurs dans pays/régions).
- `internal_norms.py` → exposition des normes internes.

### 3. **Services (`apps/api/services`)**
- `dih_score.py` → calcul basé sur `dih_principles.yml`.
- `legitimacy.py` → calcul basé sur `legitimacy_indicators.yml` + engagements.
- `internal_norms.py` → calcul basé sur `internal_norms.yml` + engagements.
- `typology.py` → classification SMP / GANE / HYBRID.
- `geo.py` → logique spatiale avec Shapely.
- `certification.py` → agrégation des scores et génération de capsules.

### 4. **Données (`data/`)**
- **Dictionaries** : YAML des principes et indicateurs.
- **Geo** : fichiers GeoJSON pour pays et régions.
- **Seeds** : JSON pour initialiser acteurs et critères.

### 5. **Démo (`apps/demo/`)**
- `app.py` → serveur FastAPI de démonstration.
- `components.py` → helpers pour formater les réponses.

---

## 🔗 Flux de certification

1. **Création d’un acteur** via `/actors/`.
2. **Ajout d’engagements** via `/engagements/`.
3. **Calcul de certification** via `/certification/{actor_id}/calculate` :
   - Lecture des principes DIH, indicateurs de légitimité et normes internes.
   - Calcul des scores individuels.
   - Agrégation pondérée en un score final.
   - Génération d’une capsule de certification.

---

## 🌍 Extension géospatiale

- Les acteurs sont associés à des coordonnées GeoJSON.
- Les endpoints `/geo/actors/in-country/{country_name}` et `/geo/actors/in-region/{region_name}` permettent de vérifier leur présence dans un polygone.
- Utilisation de **Shapely** pour les calculs spatiaux.

---

## 🧪 Tests

- `test_certification.py` → vérifie le calcul des scores.
- `test_geo.py` → valide la détection des acteurs dans une région/pays.
- `test_legitimacy.py` → teste l’impact des engagements sur la légitimité.
- `test_criteria.py` → assure le chargement correct des critères YAML.

---

## 🚀 Déploiement

- **Serveur FastAPI** avec Uvicorn.
- Données initiales chargées depuis `data/seeds/`.
- Documentation interactive disponible via `/docs`.

---

## 📌 Conclusion

L’architecture ITCAA est **modulaire, transparente et évolutive** :
- Chaque service est isolé et configurable via YAML/JSON.
- Les données géospatiales et normatives sont intégrées.
- La certification est dynamique et reflète les engagements des acteurs.
