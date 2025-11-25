// static/offline.js
const cacheKey = "itcaaGeoJSONCache";

async function preloadRegions(regions) {
  const cache = {};
  for(const r of regions){
    const url = `/export/actors/json?region=${r}`;
    try {
      const res = await fetch(url);
      const data = await res.json();
      cache[r] = data;
    } catch(e){
      console.warn("Erreur préchargement", r, e);
    }
  }
  localStorage.setItem(cacheKey, JSON.stringify(cache));
}

function getCachedRegion(region){
  const cache = JSON.parse(localStorage.getItem(cacheKey) || "{}");
  return cache[region] || [];
}

// Exemple d’utilisation
// preloadRegions(["africa","mena","americas","asia","europe"]);
