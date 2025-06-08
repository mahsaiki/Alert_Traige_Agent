from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    message = Column(String)
    status = Column(String)
    severity = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String)
    labels = Column(JSON)
    triage_status = Column(String, default="pending")
    triage_notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    history = relationship("AlertHistory", back_populates="alert")

class TriageRule(Base):
    __tablename__ = "triage_rules"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)
    conditions = Column(JSON)
    actions = Column(JSON)
    priority = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AlertHistory(Base):
    __tablename__ = "alert_history"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    status = Column(String)
    notes = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    alert = relationship("Alert", back_populates="history") 