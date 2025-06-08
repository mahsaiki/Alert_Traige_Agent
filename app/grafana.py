import os
import requests
from dotenv import load_dotenv

load_dotenv()

GRAFANA_URL = os.getenv("GRAFANA_URL")
GRAFANA_API_KEY = os.getenv("GRAFANA_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {GRAFANA_API_KEY}",
    "Content-Type": "application/json"
}

def acknowledge_alert(alert_uid: str, message: str = "Acknowledged by agent"):
    url = f"{GRAFANA_URL}/api/alertmanager/grafana/api/v2/alerts/{alert_uid}/annotations"
    data = {
        "text": message
    }
    response = requests.post(url, json=data, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def add_annotation(dashboard_uid: str, text: str, tags=None):
    url = f"{GRAFANA_URL}/api/annotations"
    data = {
        "dashboardUID": dashboard_uid,
        "text": text,
        "tags": tags or []
    }
    response = requests.post(url, json=data, headers=HEADERS)
    response.raise_for_status()
    return response.json() 