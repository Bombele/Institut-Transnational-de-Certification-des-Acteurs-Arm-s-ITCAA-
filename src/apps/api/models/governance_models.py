# apps/api/governance_models.py
from sqlalchemy import Column, Integer, String, DateTime, Enum, JSON, Boolean
from sqlalchemy.orm import declarative_base
import enum
Base = declarative_base()

class Region(enum.Enum):
    AFRICA = "africa"; AMERICAS = "americas"; ASIA = "asia"; EUROPE = "europe"; MENA = "mena"; OCEANIA = "oceania"

class AdvisoryRole(enum.Enum):
    JURIST = "jurist"; DIPLOMAT = "diplomat"; RESEARCHER = "researcher"; NGO = "ngo"; DIASPORA = "diaspora"

class AdvisoryMember(Base):
    __tablename__ = "advisory_members"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(Enum(AdvisoryRole), nullable=False)
    region = Column(Enum(Region), nullable=False)
    affiliation = Column(String)
    bio = Column(String)
    active = Column(Boolean, default=True)

class EthicsCase(Base):
    __tablename__ = "ethics_cases"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, default="open")  # open/reviewed/closed
    opened_at = Column(DateTime)
    closed_at = Column(DateTime)
    tags = Column(JSON)  # ["neutrality","bias"]

class AuditExternal(Base):
    __tablename__ = "audit_external"
    id = Column(Integer, primary_key=True)
    auditor_name = Column(String, nullable=False)
    scope = Column(String)   # "DIH protocol v1.0", "Security ISO mapping"
    report_uri = Column(String)
    conducted_at = Column(DateTime)

class FundingDisclosure(Base):
    __tablename__ = "funding_disclosures"
    id = Column(Integer, primary_key=True)
    funder = Column(String, nullable=False)
    amount = Column(Integer)
    year = Column(Integer)
    notes = Column(String)
    public = Column(Boolean, default=True)
