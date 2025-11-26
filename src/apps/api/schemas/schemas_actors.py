from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime

# 🎭 Types d’acteurs
ActorType = Literal["gane", "pmc", "militia", "hybrid"]

# 🌍 Régions
Region = Literal["africa", "americas", "asia", "europe", "mena", "oceania", "global"]

# 🧑‍💼 Acteur
class ActorBase(BaseModel):
    name: str
    type: ActorType
    region: Region
    active: Optional[bool] = True
    started_at: Optional[datetime]
    notes: Optional[str]
    meta: Optional[dict] = Field(
        default_factory=dict,
        description="Exemple : {'aliases': [...], 'territorial_control': True, 'size_estimate': '1k-5k'}"
    )

class ActorCreate(ActorBase):
    pass

class ActorRead(ActorBase):
    id: int

    class Config:
        orm_mode = True

# 🏛️ Catégories de clients
ClientCategory = Literal["UN", "UA", "EU", "OEA", "NGO", "STATE", "ENTERPRISE", "THINKTANK"]

# 🧑‍💼 Client
class ClientBase(BaseModel):
    name: str
    category: ClientCategory
    country: Optional[str]
    notes: Optional[str]

class ClientCreate(ClientBase):
    pass

class ClientRead(ClientBase):
    id: int

    class Config:
        orm_mode = True

# 🤝 Types de partenaires
PartnerType = Literal["UNIVERSITY", "THINKTANK", "FOUNDATION", "REGIONAL_ORG", "COMMUNITY"]

# 🤝 Partenaire
class PartnerBase(BaseModel):
    name: str
    type: PartnerType
    region: Optional[Region]
    notes: Optional[str]
    links: Optional[dict] = Field(
        default_factory=dict,
        description="Exemple : {'website': '...', 'mou_uri': '...'}"
    )

class PartnerCreate(PartnerBase):
    pass

class PartnerRead(PartnerBase):
    id: int

    class Config:
        orm_mode = True

# ⚠️ Types et niveaux de risque
RiskType = Literal["political_contest", "manipulation", "data_security", "neutrality", "diplomacy_fragile"]
RiskLevel = Literal["low", "medium", "high", "critical"]

# 📋 Registre des risques
class RiskRegisterBase(BaseModel):
    risk_type: RiskType
    level: RiskLevel
    description: str
    mitigation: Optional[str]
    owner: Optional[str]
    reviewed_at: Optional[datetime]

class RiskRegisterCreate(RiskRegisterBase):
    pass

class RiskRegisterRead(RiskRegisterBase):
    id: int

    class Config:
        orm_mode = True

# 🔗 Lien Acteur–Client
class ActorClientLinkBase(BaseModel):
    actor_id: int
    client_id: int
    purpose: Optional[str]
    status: Optional[str] = "active"

class ActorClientLinkCreate(ActorClientLinkBase):
    pass

class ActorClientLinkRead(ActorClientLinkBase):
    id: int

    class Config:
        orm_mode = True

# 🔗 Lien Acteur–Partenaire
class ActorPartnerLinkBase(BaseModel):
    actor_id: int
    partner_id: int
    role: Optional[str]

class ActorPartnerLinkCreate(ActorPartnerLinkBase):
    pass

class ActorPartnerLinkRead(ActorPartnerLinkBase):
    id: int

    class Config:
        orm_mode = True
