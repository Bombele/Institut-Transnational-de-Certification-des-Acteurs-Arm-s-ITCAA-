# apps/api/models_narration.py
from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

class NarrationType(enum.Enum):
    TAXONOMY = "taxonomy"
    TESTIMONY = "testimony"
    TRANSLATION = "translation"
    FUNDING = "funding"

class CitizenNarration(Base):
    __tablename__ = "citizen_narration"
    id = Column(Integer, primary_key=True)
    type = Column(Enum(NarrationType), nullable=False)
    content = Column(String, nullable=False)
    locale = Column(String, default="fr")
    contributor = Column(String)  # diaspora, communauté locale
    created_at = Column(DateTime)
    validated = Column(Boolean, default=False)
