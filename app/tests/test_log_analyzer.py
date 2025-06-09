import unittest
from unittest.mock import patch, MagicMock
import os
import json
from datetime import datetime
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))
from backend.log_analyzer import LogAnalyzer

class TestLogAnalyzer(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        # Mock environment variables
        self.env_patcher = patch.dict(os.environ, {
            'OPENROUTER_API_KEY': 'test_openrouter_key',
            'HUGGINGFACE_API_KEY': 'test_huggingface_key',
            'OPENROUTER_MODEL': 'deepseek/deepseek-r1-0528:free',
            'HUGGINGFACE_MODEL': 'mistralai/Mistral-7B-Instruct-v0.1'
        })
        self.env_patcher.start()
        
        # Create LogAnalyzer instance
        self.analyzer = LogAnalyzer()

    def tearDown(self):
        """Clean up after each test."""
        self.env_patcher.stop()

    def test_init(self):
        """Test LogAnalyzer initialization."""
        self.assertEqual(self.analyzer.openrouter_api_key, 'test_openrouter_key')
        self.assertEqual(self.analyzer.huggingface_api_key, 'test_huggingface_key')
        self.assertEqual(self.analyzer.openrouter_model, 'deepseek/deepseek-r1-0528:free')
        self.assertEqual(self.analyzer.huggingface_model, 'mistralai/Mistral-7B-Instruct-v0.1')
        self.assertIsNotNone(self.analyzer.model_configs)

    def test_analyze_logs_with_openrouter(self):
        """Test log analysis using OpenRouter."""
        # Mock OpenRouter API response
        mock_response = {
            "choices": [{
                "message": {
                    "content": json.dumps({
                        "summary": "Test summary",
                        "issues": [{
                            "description": "Test issue",
                            "severity": "Medium",
                            "recommendation": "Test recommendation",
                            "command": "test command",
                            "security_implication": "Test security"
                        }]
                    })
                }
            }]
        }
        
        with patch('requests.post') as mock_post:
            mock_post.return_value.json.return_value = mock_response
            mock_post.return_value.status_code = 200
            
            analyzer = LogAnalyzer()
            result = analyzer.analyze_logs("Test log message", model="deepseek/deepseek-r1-0528:free")
            
            self.assertIn('summary', result)
            self.assertIn('issues', result)
            self.assertEqual(len(result['issues']), 1)
            self.assertEqual(result['issues'][0]['severity'], 'Medium')

    def test_analyze_logs_with_huggingface(self):
        """Test log analysis using HuggingFace."""
        test_log = "Test log message"
        test_model = "mistralai/Mistral-7B-Instruct-v0.1"
        
        # Mock response from HuggingFace
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{
            "generated_text": json.dumps({
                "summary": "Test summary",
                "issues": [{
                    "description": "Test issue",
                    "severity": "Medium",
                    "recommendation": "Test recommendation",
                    "command": "test command",
                    "security_implication": "Test security"
                }]
            })
        }]
        
        with patch('requests.post', return_value=mock_response):
            result = self.analyzer.analyze_logs(test_log, model=test_model)
            
            self.assertIn('summary', result)
            self.assertIn('issues', result)

    def test_analyze_logs_no_api_keys(self):
        """Test log analysis with no API keys."""
        # Remove API keys
        self.analyzer.openrouter_api_key = None
        self.analyzer.huggingface_api_key = None
        
        result = self.analyzer.analyze_logs("Test log")
        self.assertIn('error', result)

    def test_parse_analysis(self):
        """Test parsing of analysis results."""
        # Pass a JSON string as would be returned by the real API
        test_response = json.dumps({
            "summary": "Test summary",
            "issues": [{
                "description": "Test issue",
                "severity": "Medium",
                "recommendation": "Test recommendation",
                "command": "test command",
                "security_implication": "Test security"
            }]
        })
        analyzer = LogAnalyzer()
        result = analyzer._parse_analysis(test_response)
        self.assertIn('summary', result)
        self.assertIn('issues', result)
        self.assertEqual(len(result['issues']), 1)
        self.assertEqual(result['issues'][0]['severity'], 'Medium')

    def test_parse_analysis_invalid_format(self):
        """Test parsing of invalid analysis format."""
        test_analysis = "Invalid format"
        result = self.analyzer._parse_analysis(test_analysis)
        self.assertIn('error', result)

if __name__ == '__main__':
    unittest.main() 