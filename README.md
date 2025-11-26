# ITCAA – Institut Transnational de Certification des Acteurs Armés

![Structure Check](https://github.com/Bombele/ITCAA/actions/workflows/structure-check.yml/badge.svg)
![Annual Report](https://github.com/Bombele/ITCAA/actions/workflows/annual_report.yml/badge.svg)
![Predeploy Check](https://github.com/Bombele/ITCAA/actions/workflows/structure-check.yml/badge.svg?branch=main&event=push)
![Deploy ITCAA API](https://github.com/Bombele/ITCAA/actions/workflows/deploy.yml/badge.svg?branch=main)
---

## 🎯 Vision
L’ITCAA est une initiative **citoyenne et institutionnelle** fondée par **Camille Bombele Liyama**.  
Elle vise à certifier les acteurs armés non étatiques selon leur conformité au **Droit International Humanitaire (DIH)**, leur **légitimité institutionnelle** et leurs **normes internes**.  
La plateforme combine **IA**, **technologies géospatiales** et **documentation narrative** pour offrir une certification transparente, traçable et évolutive.

---

## 🏗️ Architecture
- **Backend FastAPI** : endpoints pour acteurs, capsules, certification, critères, géo.
- **Services Python** : calcul des scores DIH, légitimité, normes internes, typologie.
- **Base de données SQLAlchemy** : stockage des acteurs, engagements, capsules.
- **Validation Pydantic** : cohérence et auditabilité des données.
- **Données YAML/JSON** : dictionnaires de principes et indicateurs, seeds initiaux.
- **Cartographie GeoJSON + Leaflet/Shapely** : contextualisation géographique.
- **Interfaces Jinja2 + JS léger** : SSR pour stabilité, interactivité minimale (cartes, filtres, langue).
- **Démo (`apps/demo/`)** : application illustrative avec composants réutilisables.

👉 Voir [ARCHITECTURE.md](ARCHITECTURE.md) pour plus de détails.

---

## ⚖️ Protocoles de Certification
1. **DIH** : distinction, proportionnalité, nécessité, humanité.  
2. **Légitimité** : reconnaissance communautaire, non-discrimination, responsabilité interne, traçabilité.  
3. **Normes internes** : codes de conduite, chartes communautaires, engagements humanitaires.  
4. **Géospatial** : localisation des acteurs dans pays/régions sensibles.  

👉 Voir [CERTIFICATION_PROTOCOL.md](CERTIFICATION_PROTOCOL.md).

---

## 🌍 Éthique et DIH
- Les acteurs sont à la fois **sujets du DIH** et **créateurs de normes internes**.  
- L’IA croise engagements documentés et principes normatifs.  
- Les nouvelles technologies assurent transparence et traçabilité.  

👉 Voir [ETHICS_AND_DIH.md](ETHICS_AND_DIH.md).

---

## 🚀 Déploiement
- **Local** : Uvicorn + FastAPI  
- **Docker** : conteneurisation pour portabilité  
- **Cloud** : Render, Hugging Face Spaces, Railway  
- **CI/CD** : GitHub Actions pour tests et déploiement automatisés  

👉 Voir [DEPLOYMENT.md](DEPLOYMENT.md).

---

## 🖥️ Interfaces
### Interface institutionnelle
- SSR avec Jinja2 + JS léger  
- Cartographie interactive (Leaflet + GeoJSON)  
- Rapports multilingues (PDF, HTML)  
- Gouvernance : conseil, alliances, rapports consultatifs  
- LexCivic : soumission citoyenne + certification  

### Interface interactive
- Mode hors-ligne : cache GeoJSON par région  
- Recherche avancée côté client : filtrage instantané, tri par score ou alphabétique  
- UX améliorée sans frameworks lourds  

### Interface citoyenne
- Multilinguisme stratégique : fichiers `data/i18n/{en,fr,es,ar,ru,zh}.json`  
- Sélecteur global de langue  
- Accessibilité : contraste, focus visible, navigation simple  
- Sécurité : RBAC, audit middleware, segmentation des données sensibles  

---

## 🧑‍💻 Développeur principal
- **Camille Bombele Liyama**  
  - Fondateur et architecte institutionnel  
  - Développeur principal (FastAPI, SQLAlchemy, CI/CD, multilinguisme, i18n)
