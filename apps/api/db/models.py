# apps/api/db/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .base import Base

class Actor(Base):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    acronym = Column(String)
    typology = Column(String)  # SMP | GANE | HYBRID
    country = Column(String)
    region = Column(String)
    geojson = Column(JSON)
    active_from = Column(DateTime)
    active_to = Column(DateTime)

    engagements = relationship("Engagement", back_populates="actor")
    capsules = relationship("Capsule", back_populates="actor")

class Engagement(Base):
    __tablename__ = "engagements"
    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id"))
    title = Column(String)
    description = Column(String)
    category = Column(String)  # ethics | DIH | community
    evidence = Column(JSON)
    date = Column(DateTime)

    actor = relationship("Actor", back_populates="engagements")

class Capsule(Base):
    __tablename__ = "capsules"
    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id"))
    narrative = Column(String)
    legitimacy_score = Column(Float)
    dih_score = Column(Float)
    certification_score = Column(Float)
    version = Column(String)
    validations = Column(JSON)
    published_at = Column(DateTime)

    actor = relationship("Actor", back_populates="capsules")
