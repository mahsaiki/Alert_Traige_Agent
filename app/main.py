from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, crud, grafana
from app.database import engine, get_db
import logging
from datetime import datetime
import uvicorn

models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Alert Triage Agent",
    description="An intelligent alert management system for Grafana",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Alert Triage Agent API"}

@app.post("/api/v1/alerts", response_model=schemas.AlertOut)
def receive_alert(alert: schemas.AlertIn, db: Session = Depends(get_db)):
    try:
        logger.info(f"Received alert: {alert.title}")
        db_alert = crud.create_alert(db, alert)
        # Optionally acknowledge in Grafana
        # grafana.acknowledge_alert(alert_uid, message="Received by agent")
        return db_alert
    except Exception as e:
        logger.error(f"Error processing alert: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/alerts", response_model=List[schemas.AlertOut])
def get_alerts(db: Session = Depends(get_db)):
    return crud.get_alerts(db)

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@app.post("/api/v1/triage_rules", response_model=schemas.TriageRuleOut)
def create_triage_rule(rule: schemas.TriageRuleIn, db: Session = Depends(get_db)):
    return crud.create_triage_rule(db, rule)

@app.get("/api/v1/triage_rules", response_model=List[schemas.TriageRuleOut])
def get_triage_rules(db: Session = Depends(get_db)):
    return crud.get_triage_rules(db)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 