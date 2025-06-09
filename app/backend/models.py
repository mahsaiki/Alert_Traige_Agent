from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    message = Column(String)
    status = Column(String)
    severity = Column(String)
    timestamp = Column(String)
    source = Column(String)
    labels = Column(JSON)

class TriageRule(Base):
    __tablename__ = 'triage_rules'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    conditions = Column(JSON)
    actions = Column(JSON)
    priority = Column(Integer)
    is_active = Column(Boolean, default=True) 