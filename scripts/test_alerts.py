import requests
import json
from datetime import datetime
import random

# Test configuration
API_URL = "http://localhost:8000/api/v1"
TEST_ALERTS = [
    {
        "title": "High CPU Usage",
        "message": "CPU usage is above 90% for the last 5 minutes",
        "status": "firing",
        "severity": "critical",
        "timestamp": datetime.utcnow().isoformat(),
        "source": "grafana",
        "labels": {
            "instance": "server-1",
            "job": "node_exporter"
        }
    },
    {
        "title": "Memory Warning",
        "message": "Memory usage is above 80%",
        "status": "warning",
        "severity": "warning",
        "timestamp": datetime.utcnow().isoformat(),
        "source": "grafana",
        "labels": {
            "instance": "server-2",
            "job": "node_exporter"
        }
    },
    {
        "title": "Disk Space Alert",
        "message": "Disk space is running low",
        "status": "firing",
        "severity": "critical",
        "timestamp": datetime.utcnow().isoformat(),
        "source": "grafana",
        "labels": {
            "instance": "server-1",
            "job": "node_exporter"
        }
    }
]

def test_create_alert(alert_data):
    """Test creating a single alert"""
    try:
        response = requests.post(f"{API_URL}/alerts", json=alert_data)
        response.raise_for_status()
        print(f"✅ Successfully created alert: {alert_data['title']}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to create alert: {str(e)}")
        return None

def test_get_alerts():
    """Test retrieving all alerts"""
    try:
        response = requests.get(f"{API_URL}/alerts")
        response.raise_for_status()
        alerts = response.json()
        print(f"✅ Successfully retrieved {len(alerts)} alerts")
        return alerts
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get alerts: {str(e)}")
        return None

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{API_URL}/health")
        response.raise_for_status()
        print("✅ Health check successful")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {str(e)}")
        return None

def main():
    print("🚀 Starting Alert Triage Agent Tests")
    print("-" * 50)

    # Test health check
    print("\nTesting health check...")
    health = test_health_check()
    if not health:
        print("❌ Health check failed, aborting tests")
        return

    # Test creating alerts
    print("\nTesting alert creation...")
    created_alerts = []
    for alert in TEST_ALERTS:
        result = test_create_alert(alert)
        if result:
            created_alerts.append(result)

    # Test retrieving alerts
    print("\nTesting alert retrieval...")
    alerts = test_get_alerts()
    if alerts:
        print("\nRetrieved Alerts:")
        for alert in alerts:
            print(f"- {alert['title']} ({alert['severity']})")

    print("\n✨ Test Summary:")
    print(f"- Health Check: {'✅' if health else '❌'}")
    print(f"- Alerts Created: {len(created_alerts)}/{len(TEST_ALERTS)}")
    print(f"- Alerts Retrieved: {len(alerts) if alerts else 0}")

if __name__ == "__main__":
    main() 