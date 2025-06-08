import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import json

# Add the app directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.backend.log_analyzer import LogAnalyzer

class TestLogAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = LogAnalyzer()
        self.sample_log_path = os.path.join(os.path.dirname(__file__), 'sample.log')
        
        # Read sample log file
        with open(self.sample_log_path, 'r') as f:
            self.sample_log = f.read()

    def test_preprocess_logs(self):
        """Test log preprocessing functionality"""
        processed_log = self.analyzer.preprocess_logs(self.sample_log)
        self.assertIsInstance(processed_log, str)
        self.assertNotIn('\n\n', processed_log)  # No double newlines
        self.assertTrue(len(processed_log) > 0)

    @patch('requests.post')
    def test_analyze_with_openrouter(self, mock_post):
        """Test OpenRouter API integration"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': json.dumps({
                        'summary': 'Test summary',
                        'issues': [
                            {
                                'description': 'Test issue',
                                'severity': 'high',
                                'recommendation': 'Test recommendation',
                                'command': 'test command',
                                'security_implication': 'Test security implication'
                            }
                        ]
                    })
                }
            }]
        }
        mock_post.return_value = mock_response

        # Set OpenRouter API key
        os.environ['OPENROUTER_API_KEY'] = 'test_key'
        
        result = self.analyzer.analyze_with_openrouter(self.sample_log)
        self.assertIsInstance(result, dict)
        self.assertIn('summary', result)
        self.assertIn('issues', result)

    @patch('requests.post')
    def test_analyze_with_huggingface(self, mock_post):
        """Test HuggingFace API integration"""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = [{
            'generated_text': json.dumps({
                'summary': 'Test summary',
                'issues': [
                    {
                        'description': 'Test issue',
                        'severity': 'high',
                        'recommendation': 'Test recommendation',
                        'command': 'test command',
                        'security_implication': 'Test security implication'
                    }
                ]
            })
        }]
        mock_post.return_value = mock_response

        # Set HuggingFace API key
        os.environ['HUGGINGFACE_API_KEY'] = 'test_key'
        
        result = self.analyzer.analyze_with_huggingface(self.sample_log)
        self.assertIsInstance(result, dict)
        self.assertIn('summary', result)
        self.assertIn('issues', result)

    def test_error_handling(self):
        """Test error handling with invalid log format"""
        invalid_log = "Invalid log format"
        result = self.analyzer.analyze_logs(invalid_log)
        self.assertIsInstance(result, dict)
        self.assertIn('error', result)

    def test_severity_detection(self):
        """Test severity detection for common log patterns"""
        # Test SSH failure detection
        ssh_log = "Failed password for user root from 192.168.1.100"
        severity = self.analyzer._determine_severity(ssh_log)
        self.assertEqual(severity, 'high')

        # Test CPU warning detection
        cpu_log = "CPU temperature above threshold, cpu clock throttled"
        severity = self.analyzer._determine_severity(cpu_log)
        self.assertEqual(severity, 'medium')

        # Test normal log detection
        normal_log = "Started Daily apt download activities"
        severity = self.analyzer._determine_severity(normal_log)
        self.assertEqual(severity, 'low')

if __name__ == '__main__':
    unittest.main() 