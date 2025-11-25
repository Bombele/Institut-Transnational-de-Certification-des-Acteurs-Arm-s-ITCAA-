# apps/api/routers/export.py
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse, JSONResponse
from sqlalchemy.orm import Session
import csv, io
from apps.api.database import SessionLocal
from apps.api.models_cartography import Actor, Region, ActorType

router = APIRouter(prefix="/export", tags=["export"])

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@router.get("/actors/json")
def export_json(
    db: Session = Depends(get_db),
    region: Region | None = Query(None),
    type: ActorType | None = Query(None)
):
    query = db.query(Actor)
    if region: query = query.filter(Actor.region == region)
    if type: query = query.filter(Actor.type == type)
    actors = query.all()
    data = [
        {
            "id": a.id,
            "name": a.name,
            "type": a.type.value,
            "region": a.region.value,
            "status": a.status.value,
            "aliases": a.aliases,
            "languages": a.languages
        }
        for a in actors
    ]
    return JSONResponse(content=data)

@router.get("/actors/csv")
def export_csv(
    db: Session = Depends(get_db),
    region: Region | None = Query(None),
    type: ActorType | None = Query(None)
):
    query = db.query(Actor)
    if region: query = query.filter(Actor.region == region)
    if type: query = query.filter(Actor.type == type)
    actors = query.all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id","name","type","region","status","aliases","languages"])
    for a in actors:
        writer.writerow([
            a.id, a.name, a.type.value, a.region.value, a.status.value,
            ";".join(a.aliases or []), ";".join(a.languages or [])
        ])
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv",
                             headers={"Content-Disposition":"attachment; filename=actors.csv"})
