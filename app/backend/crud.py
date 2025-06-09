from sqlalchemy.orm import Session
from . import models, schemas

def create_alert(db: Session, alert: 'schemas.AlertIn'):
    db_alert = models.Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

def get_alerts(db: Session):
    return db.query(models.Alert).all()

def create_triage_rule(db: Session, rule: 'schemas.TriageRuleIn'):
    db_rule = models.TriageRule(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

def get_triage_rules(db: Session):
    return db.query(models.TriageRule).all() 