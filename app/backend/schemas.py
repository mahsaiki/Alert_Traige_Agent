from pydantic import BaseModel
from typing import Optional, Dict, Any

class AlertIn(BaseModel):
    title: str
    message: str
    status: str
    severity: str
    timestamp: str
    source: str
    labels: Optional[Dict[str, Any]] = None

class AlertOut(AlertIn):
    id: int

class TriageRuleIn(BaseModel):
    name: str
    description: str
    conditions: Dict[str, Any]
    actions: Dict[str, Any]
    priority: int
    is_active: bool = True

class TriageRuleOut(TriageRuleIn):
    id: int 