# apps/api/models_reports.py
from sqlalchemy import Column, Integer, String, DateTime, JSON, Enum
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

class Language(enum.Enum):
    EN = "en"; FR = "fr"; ES = "es"; AR = "ar"; RU = "ru"; ZH = "zh"
    LN = "ln"; SW = "sw"; PT = "pt"  # langues régionales

class AnnualReport(Base):
    __tablename__ = "annual_reports"
    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    languages = Column(JSON)  # ["en","fr","es","ar","ru","zh","ln","sw","pt"]
    stats = Column(JSON)      # {"certifications": {...}, "dih_indicators": {...}}
    case_studies = Column(JSON)
    testimonies = Column(JSON)
    published_at = Column(DateTime)
    uri = Column(String)      # lien vers PDF/HTML
