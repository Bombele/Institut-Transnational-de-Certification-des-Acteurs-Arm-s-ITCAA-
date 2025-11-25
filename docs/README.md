# ITCAA – Institut Transnational de Certification des Acteurs Armés

## 🎯 Vision
L’ITCAA est une plateforme de **justice digitale** qui vise à certifier les acteurs armés non étatiques en fonction de leur conformité au **Droit International Humanitaire (DIH)**, de leur **légitimité institutionnelle** et de leurs **normes internes**.  
Elle combine **intelligence artificielle (IA)**, **technologies géospatiales** et **documentation narrative** pour offrir une certification transparente, traçable et évolutive.

---

## 🏗️ Architecture
- **API FastAPI** : endpoints pour acteurs, capsules, certification, critères, géo.
- **Services Python** : calcul des scores DIH, légitimité, normes internes, typologie.
- **Base de données SQLAlchemy** : stockage des acteurs, engagements, capsules.
- **Données YAML/JSON** : dictionnaires de principes et indicateurs, seeds initiaux.
- **GeoJSON + Shapely** : contextualisation géographique des acteurs.
- **Démo (`apps/demo/`)** : application illustrative avec composants réutilisables.

👉 Voir [ARCHITECTURE.md](ARCHITECTURE.md) pour plus de détails.

---

## ⚖️ Protocoles de Certification
L’ITCAA propose plusieurs protocoles modulaires :
1. **DIH** : distinction, proportionnalité, nécessité, humanité.
2. **Légitimité** : reconnaissance communautaire, non-discrimination, responsabilité interne, traçabilité.
3. **Normes internes** : codes de conduite, chartes communautaires, engagements humanitaires.
4. **Géospatial** : localisation des acteurs dans pays/régions sensibles.

👉 Voir [CERTIFICATION_PROTOCOL.md](CERTIFICATION_PROTOCOL.md).

---

## 🌍 Éthique et DIH
L’ITCAA articule **éthique** et **DIH** :
- Les acteurs sont à la fois **sujets du DIH** et **créateurs de normes internes**.
- L’IA croise engagements documentés et principes normatifs.
- Les nouvelles technologies assurent transparence et traçabilité.

👉 Voir [ETHICS_AND_DIH.md](ETHICS_AND_DIH.md).

---

## 🚀 Déploiement
- **Local** : Uvicorn + FastAPI.
- **Docker** : conteneurisation pour portabilité.
- **Cloud** : Render, Hugging Face Spaces, Railway.
- **CI/CD** : GitHub Actions pour tests et déploiement automatisés.

👉 Voir [DEPLOYMENT.md](DEPLOYMENT.md).

---

## 📌 Conclusion
L’ITCAA est une initiative **transnationale et innovante** :
- Allie **IA, DIH et éthique**.
- Offre une certification **modulaire et transparente**.
- Sert de mémoire institutionnelle pour la diaspora et les générations futures.
# ITCAA – Interface institutionnelle (FastAPI + Jinja2 + JavaScript léger)

## Objectif
Interface neutre, multilingue et accessible, avec SSR pour la stabilité et une couche JavaScript légère pour l’interactivité (carte, filtres, langue).

## Lancer
- `uvicorn apps.api.main:app --reload`
- Accueil: `/ui/?lang=fr`
- Carte: `/ui/map?lang=fr`

## Modules
- Accueil: sélection de langue, navigation, mission
- Cartographie: Leaflet + GeoJSON, filtres par région/type, export CSV/JSON
- Acteurs: liste SSR + filtre client, fiche avec scores DIH/relations/GeoJSON/PDF
- Rapports: bibliothèque multilingue (PDF)
- Gouvernance: conseil, alliances, rapports consultatifs
- LexCivic: soumission citoyenne + liste

## Multilingue
- Fichiers `data/i18n/{en,fr,es,ar,ru,zh}.json` (fallback en)
- Sélecteur de langue global (JS)

## Exports et Rapports
- JSON: `/export/actors/json?region=&type=`
- CSV: `/export/actors/csv?region=&type=`
- PDF acteur: `/reports/actor/{id}/pdf?lang=fr`

## Accessibilité
- Contraste, focus visible (CSS), forms labellisés, navigation simple

## Sécurité
- RBAC sur routes d’écriture (certification, narration)
- Audit middleware, segmentation des données sensibles

## Pourquoi du JavaScript (léger) ici
- Carte interactive (Leaflet) et filtres dynamiques
- Meilleure UX (sélecteur de langue, filtrage client, feedback)
- Tout reste transparent: données servies par API, JS sans frameworks lourds
