# apps/api/db/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class EngagementBase(BaseModel):
    title: str
    description: str
    category: str
    evidence: Optional[List[dict]]
    date: datetime

class CapsuleBase(BaseModel):
    narrative: str
    legitimacy_score: float
    dih_score: float
    certification_score: float
    version: str
    validations: Optional[List[dict]]
    published_at: datetime

class ActorBase(BaseModel):
    name: str
    acronym: Optional[str]
    typology: str
    country: str
    region: Optional[str]
    geojson: Optional[dict]
    active_from: Optional[datetime]
    active_to: Optional[datetime]

class ActorCreate(ActorBase):
    pass

class ActorOut(ActorBase):
    id: int
    class Config:
        orm_mode = True
