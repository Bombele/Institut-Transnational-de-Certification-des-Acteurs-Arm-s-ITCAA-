# apps/api/models_diplomacy.py
from sqlalchemy import Column, Integer, String, DateTime, Enum, JSON, Boolean
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

class PartnerCategory(enum.Enum):
    REGIONAL_ORG = "regional_org"
    NGO = "ngo"

class Alliance(Base):
    __tablename__ = "alliances"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(Enum(PartnerCategory), nullable=False)
    region = Column(String)  # "Africa","Europe","Americas","Asia"
    modalities = Column(JSON)  # {"MoU":True,"joint_reports":True,"forums":True}
    signed_at = Column(DateTime)
    active = Column(Boolean, default=True)
    notes = Column(String)
