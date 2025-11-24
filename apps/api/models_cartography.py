# apps/api/models_cartography.py
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey, JSON, Float
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

class Region(enum.Enum):
    AFRICA = "africa"; MENA = "mena"; AMERICAS = "americas"; ASIA = "asia"; EUROPE = "europe"; GLOBAL = "global"

class ActorType(enum.Enum):
    GANE = "gane"      # Groupe armé non étatique
    PMC = "pmc"        # Société militaire privée
    MILITIA = "militia"
    HYBRID = "hybrid"

class ActorStatus(enum.Enum):
    ACTIVE = "active"; INACTIVE = "inactive"; DISSIDENT = "dissident"; TRANSFORMING = "transforming"

class Actor(Base):
    __tablename__ = "actors"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    type = Column(Enum(ActorType), nullable=False)
    region = Column(Enum(Region), nullable=False)
    status = Column(Enum(ActorStatus), default=ActorStatus.ACTIVE)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    aliases = Column(JSON)              # ["Houthis","Ansar Allah"]
    leadership = Column(JSON)           # [{"name":"X","role":"leader"}]
    org_structure = Column(JSON)        # {"cells":"decentralized","command":"hierarchical"}
    size_estimate = Column(String)      # "1k-5k"
    funding_sources = Column(JSON)      # ["contracts","natural_resources","illicit_trafficking"]
    languages = Column(JSON)            # ["ar","en"]
    notes = Column(String)              # prudence : pas d’info sensible au public

class InfluenceZone(Base):
    __tablename__ = "influence_zones"
    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id"), nullable=False)
    country = Column(String, index=True)
    province = Column(String)
    cross_border = Column(Boolean, default=False)
    geojson = Column(JSON)              # FeatureCollection
    updated_at = Column(DateTime)
    actor = relationship("Actor", backref="zones")

class RelationType(enum.Enum):
    ALLIANCE = "alliance"; CONFLICT = "conflict"; STATE_LINK = "state_link"; ENTERPRISE_LINK = "enterprise_link"

class ActorRelation(Base):
    __tablename__ = "actor_relations"
    id = Column(Integer, primary_key=True)
    source_actor_id = Column(Integer, ForeignKey("actors.id"), nullable=False)
    target_name = Column(String, nullable=False)  # autre acteur / État / entreprise
    relation_type = Column(Enum(RelationType), nullable=False)
    details = Column(String)
    updated_at = Column(DateTime)

class DIHIndicator(Base):
    __tablename__ = "dih_indicators"
    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id"), nullable=False)
    indicator_key = Column(String, nullable=False)  # "distinction","proportionality",...
    value = Column(Float, nullable=False)           # 0.0-1.0 (respect/violation inversé selon design)
    weight = Column(Float, nullable=False)          # pondération protocolaire
    version = Column(String, default="v1.0")
    computed_at = Column(DateTime)

class ActorScore(Base):
    __tablename__ = "actor_scores"
    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id"), nullable=False)
    dih_score = Column(Float)
    legitimacy_score = Column(Float)
    norms_score = Column(Float)
    total_score = Column(Float)
    status = Column(String)  # "certified"/"provisional"/"not_certified"
    version = Column(String, default="v1.0")
    computed_at = Column(DateTime)
