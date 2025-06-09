import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import Session
from backend import crud, models, schemas

class TestCRUD(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)

    def test_create_alert(self):
        alert_data = schemas.AlertIn(
            title="Test Alert",
            message="Test Message",
            status="active",
            severity="high",
            timestamp="2023-01-01T00:00:00",
            source="test_source",
            labels={"key": "value"}
        )
        db_alert = crud.create_alert(self.db, alert_data)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    def test_get_alerts(self):
        crud.get_alerts(self.db)
        self.db.query.assert_called_once_with(models.Alert)

    def test_create_triage_rule(self):
        rule_data = schemas.TriageRuleIn(
            name="Test Rule",
            description="Test Description",
            conditions={"key": "value"},
            actions={"action": "value"},
            priority=1,
            is_active=True
        )
        db_rule = crud.create_triage_rule(self.db, rule_data)
        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

    def test_get_triage_rules(self):
        crud.get_triage_rules(self.db)
        self.db.query.assert_called_once_with(models.TriageRule)

if __name__ == '__main__':
    unittest.main() 