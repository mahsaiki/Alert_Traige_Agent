from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

class AlertIn(BaseModel):
    title: str
    message: str
    status: str
    severity: str
    timestamp: datetime
    source: str
    labels: Optional[Dict] = None

class AlertOut(AlertIn):
    id: int
    triage_status: str
    triage_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class TriageRuleIn(BaseModel):
    name: str
    description: Optional[str] = None
    conditions: Dict
    actions: Dict
    priority: int = 0
    is_active: bool = True

class TriageRuleOut(TriageRuleIn):
    id: int
    created_at: datetime
    updated_at: datetime 