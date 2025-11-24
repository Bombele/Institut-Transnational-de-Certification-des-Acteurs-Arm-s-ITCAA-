# apps/api/models_governance.py
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, JSON
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

class AdvisoryRole(enum.Enum):
    JURIST = "jurist"
    DIPLOMAT = "diplomat"
    RESEARCHER = "researcher"
    NGO = "ngo"
    DIASPORA = "diaspora"

class AdvisoryMember(Base):
    __tablename__ = "advisory_members"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(Enum(AdvisoryRole), nullable=False)
    affiliation = Column(String)
    region = Column(String)
    mandate_start = Column(DateTime)
    mandate_end = Column(DateTime)
    active = Column(Boolean, default=True)

class AdvisoryReport(Base):
    __tablename__ = "advisory_reports"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    languages = Column(JSON)  # ["en","fr","es","ar","ru","zh"]
    published_at = Column(DateTime)
    public = Column(Boolean, default=True)
