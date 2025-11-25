// static/search.js
function filterActors(actors, {q, region, type, status}){
  return actors.filter(a => {
    if(q && !a.name.toLowerCase().includes(q.toLowerCase())) return false;
    if(region && a.region !== region) return false;
    if(type && a.type !== type) return false;
    if(status && a.status !== status) return false;
    return true;
  });
}

function sortActors(actors, sortBy){
  if(sortBy === "name") return actors.sort((a,b)=>a.name.localeCompare(b.name));
  if(sortBy === "score") return actors.sort((a,b)=>b.score_total - a.score_total);
  return actors;
}

// Exemple d’utilisation
// const results = sortActors(filterActors(allActors, {q:"wagner", region:"africa"}), "score");
