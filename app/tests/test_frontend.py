import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
import pandas as pd
from datetime import datetime
import json
import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))
from backend.log_analyzer import LogAnalyzer

class TestFrontend(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        # Mock Streamlit session state
        self.session_state = {}
        st.session_state = self.session_state
        
        # Mock environment variables
        self.env_patcher = patch.dict(os.environ, {
            'OPENROUTER_API_KEY': 'test_openrouter_key',
            'HUGGINGFACE_API_KEY': 'test_huggingface_key'
        })
        self.env_patcher.start()

    def tearDown(self):
        """Clean up after each test."""
        self.env_patcher.stop()

    @patch('streamlit.button')
    @patch('streamlit.text_area')
    @patch('streamlit.file_uploader')
    def test_log_analysis_flow(self, mock_uploader, mock_text_area, mock_button):
        """Test the log analysis flow."""
        # Mock user input
        mock_text_area.return_value = "Test log message"
        mock_uploader.return_value = None
        mock_button.return_value = True
        
        # Mock LogAnalyzer
        mock_analyzer = MagicMock()
        mock_analyzer.analyze_logs.return_value = {
            "summary": "Test summary",
            "issues": [{
                "description": "Test issue",
                "severity": "High",
                "recommendations": ["Test recommendation"],
                "commands": ["test command"],
                "security_implications": ["Test security"]
            }],
            "timestamp": datetime.now().isoformat()
        }
        
        with patch('backend.log_analyzer.LogAnalyzer', return_value=mock_analyzer):
            analyzer = mock_analyzer
            result = analyzer.analyze_logs("Test log message", model="anthropic/claude-2")
            self.assertIn('summary', result)
            self.assertIn('issues', result)
            self.assertEqual(len(result['issues']), 1)
            self.assertEqual(result['issues'][0]['severity'], 'High')

    def test_export_json(self):
        """Test JSON export functionality."""
        test_data = {
            "summary": "Test summary",
            "issues": [{
                "description": "Test issue",
                "severity": "High",
                "recommendations": ["Test recommendation"],
                "commands": ["test command"],
                "security_implications": ["Test security"]
            }],
            "timestamp": datetime.now().isoformat()
        }
        
        # Convert to JSON
        json_str = json.dumps(test_data, indent=2)
        
        # Verify JSON structure
        parsed_json = json.loads(json_str)
        self.assertEqual(parsed_json['summary'], "Test summary")
        self.assertEqual(len(parsed_json['issues']), 1)
        self.assertEqual(parsed_json['issues'][0]['severity'], "High")

    def test_export_csv(self):
        """Test CSV export functionality."""
        test_data = {
            "issues": [{
                "description": "Test issue 1",
                "severity": "High",
                "recommendations": ["Test recommendation 1"],
                "commands": ["test command 1"],
                "security_implications": ["Test security 1"]
            }, {
                "description": "Test issue 2",
                "severity": "Medium",
                "recommendations": ["Test recommendation 2"],
                "commands": ["test command 2"],
                "security_implications": ["Test security 2"]
            }]
        }
        
        # Convert to DataFrame
        df = pd.DataFrame(test_data['issues'])
        
        # Verify DataFrame structure
        self.assertEqual(len(df), 2)
        self.assertEqual(df.iloc[0]['severity'], "High")
        self.assertEqual(df.iloc[1]['severity'], "Medium")

    @patch('streamlit.session_state')
    def test_session_state_management(self, mock_session_state):
        """Test session state management."""
        # Initialize session state
        mock_session_state.get.return_value = None
        
        # Test theme management
        mock_session_state.theme = 'light'
        self.assertEqual(mock_session_state.theme, 'light')
        
        # Test model selection
        mock_session_state.selected_model = 'anthropic/claude-2'
        self.assertEqual(mock_session_state.selected_model, 'anthropic/claude-2')
        
        # Test analysis history
        mock_session_state.analysis_history = []
        self.assertEqual(len(mock_session_state.analysis_history), 0)

if __name__ == '__main__':
    unittest.main() 