# apps/api/models_forums.py
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

class ForumCity(enum.Enum):
    GENEVA = "Geneva"; ADDIS = "Addis-Abeba"; BRUSSELS = "Brussels"; NEWYORK = "New York"

class ForumPresence(Base):
    __tablename__ = "forum_presence"
    id = Column(Integer, primary_key=True)
    city = Column(Enum(ForumCity), nullable=False)
    event = Column(String)        # "Panel on Peace & Security"
    format = Column(String)       # "panel","side-event","collaboration"
    partners = Column(String)     # "CICR, Geneva Academy"
    date = Column(DateTime)
    notes = Column(String)
