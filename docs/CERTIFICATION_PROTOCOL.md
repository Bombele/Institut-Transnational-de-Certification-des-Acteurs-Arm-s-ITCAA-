# ITCAA – Protocoles de Certification

## 🎯 Objectif
Les protocoles de certification de l’ITCAA visent à évaluer les acteurs armés non étatiques selon des critères normatifs, éthiques et communautaires.  
Ils doivent allier **intelligence artificielle (IA)** et **nouvelles technologies** pour garantir :
- Transparence
- Traçabilité
- Adaptabilité aux contextes locaux
- Légitimité institutionnelle

---

## 🏗️ Structure des protocoles

### 1. Protocole DIH (Droit International Humanitaire)
- Basé sur `dih_principles.yml` (distinction, proportionnalité, nécessité, humanité).
- L’IA analyse les engagements documentés et les compare aux principes DIH.
- Les scores sont calculés automatiquement et intégrés dans une capsule de certification.

### 2. Protocole de Légitimité
- Basé sur `legitimacy_indicators.yml` (reconnaissance communautaire, non-discrimination, responsabilité interne, traçabilité).
- L’IA croise les **engagements normatifs** des acteurs avec les indicateurs YAML.
- Les nouvelles technologies (API, blockchain) assurent la traçabilité des preuves.

### 3. Protocole des Normes Internes
- Basé sur `internal_norms.yml` (codes de conduite, règles disciplinaires, chartes communautaires, engagements humanitaires).
- Reconnaît que les acteurs armés sont aussi **créateurs de normes** influençant le DIH.
- L’IA détecte et pondère ces normes internes pour ajuster le score de certification.

### 4. Protocole Géospatial
- Utilise `countries.geojson` et `regions.geojson`.
- Vérifie la présence des acteurs dans des zones sensibles via **Shapely**.
- Permet de contextualiser la certification selon la localisation.

---

## 🔗 Intégration IA + Technologie

- **IA (Python + FastAPI + NLP)** : analyse des engagements, classification typologique, calcul des scores.  
- **GeoJSON + Shapely** : vérification spatiale des acteurs.  
- **Blockchain / Ledger distribué (optionnel)** : enregistrement immuable des capsules de certification.  
- **API REST** : exposition des résultats pour les institutions et la diaspora.  
- **Open Data YAML/JSON** : configuration transparente des critères et indicateurs.  

---

## 🧪 Exemple de Capsule de Certification

```json
{
  "actor": "Forces de Résistance du Kivu",
  "protocols": ["DIH", "Legitimacy", "Internal Norms", "Geo"],
  "scores": {
    "dih_score": 0.8,
    "legitimacy_score": 0.85,
    "internal_norms_score": 0.7,
    "geo_context": "Kivu"
  },
  "certification_score": 0.78,
  "version": "v2.0",
  "validations": [
    { "source": "ITCAA", "status": "calculé" },
    { "source": "Blockchain", "status": "enregistré" }
  ]
}
