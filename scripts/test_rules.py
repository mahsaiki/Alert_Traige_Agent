import requests
import json
from datetime import datetime

# Test configuration
API_URL = "http://localhost:8000/api/v1"
TEST_RULES = [
    {
        "name": "Critical CPU Rule",
        "description": "Automatically acknowledge critical CPU alerts",
        "conditions": {
            "severity": "critical",
            "title_contains": "CPU"
        },
        "actions": {
            "acknowledge": True,
            "notify": True
        },
        "priority": 1,
        "is_active": True
    },
    {
        "name": "Memory Warning Rule",
        "description": "Handle memory warnings",
        "conditions": {
            "severity": "warning",
            "title_contains": "Memory"
        },
        "actions": {
            "acknowledge": False,
            "notify": True
        },
        "priority": 2,
        "is_active": True
    }
]

def test_create_rule(rule_data):
    """Test creating a single triage rule"""
    try:
        response = requests.post(f"{API_URL}/triage_rules", json=rule_data)
        response.raise_for_status()
        print(f"✅ Successfully created rule: {rule_data['name']}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to create rule: {str(e)}")
        return None

def test_get_rules():
    """Test retrieving all triage rules"""
    try:
        response = requests.get(f"{API_URL}/triage_rules")
        response.raise_for_status()
        rules = response.json()
        print(f"✅ Successfully retrieved {len(rules)} rules")
        return rules
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get rules: {str(e)}")
        return None

def main():
    print("🚀 Starting Triage Rules Tests")
    print("-" * 50)

    # Test creating rules
    print("\nTesting rule creation...")
    created_rules = []
    for rule in TEST_RULES:
        result = test_create_rule(rule)
        if result:
            created_rules.append(result)

    # Test retrieving rules
    print("\nTesting rule retrieval...")
    rules = test_get_rules()
    if rules:
        print("\nRetrieved Rules:")
        for rule in rules:
            print(f"- {rule['name']} (Priority: {rule['priority']})")

    print("\n✨ Test Summary:")
    print(f"- Rules Created: {len(created_rules)}/{len(TEST_RULES)}")
    print(f"- Rules Retrieved: {len(rules) if rules else 0}")

if __name__ == "__main__":
    main() 