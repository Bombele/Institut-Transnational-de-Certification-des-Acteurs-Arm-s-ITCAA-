# apps/api/schemas/governance.py
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class Region(str, Enum):
    africa = "africa"
    americas = "americas"
    asia = "asia"
    europe = "europe"
    mena = "mena"
    oceania = "oceania"

class AdvisoryRole(str, Enum):
    jurist = "jurist"
    diplomat = "diplomat"
    researcher = "researcher"
    ngo = "ngo"
    diaspora = "diaspora"

class AdvisoryMemberCreate(BaseModel):
    name: str
    role: AdvisoryRole
    region: Region
    affiliation: Optional[str]
    bio: Optional[str]

class AdvisoryMemberOut(BaseModel):
    id: int
    name: str
    role: AdvisoryRole
    region: Region
    affiliation: Optional[str]
    bio: Optional[str]
    active: bool

    class Config:
        orm_mode = True

class EthicsCaseCreate(BaseModel):
    title: str
    description: str
    tags: Optional[List[str]]

class EthicsCaseOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    tags: Optional[List[str]]

    class Config:
        orm_mode = True

class AuditExternalCreate(BaseModel):
    auditor_name: str
    scope: str
    report_uri: Optional[str]

class AuditExternalOut(BaseModel):
    id: int
    auditor_name: str
    scope: str
    report_uri: Optional[str]
    conducted_at: str

    class Config:
        orm_mode = True

class FundingDisclosureCreate(BaseModel):
    funder: str
    amount: int
    year: int
    notes: Optional[str]
    public: bool = True

class FundingDisclosureOut(BaseModel):
    id: int
    funder: str
    amount: int
    year: int
    notes: Optional[str]
    public: bool

    class Config:
        orm_mode = True
