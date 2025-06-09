import os
from typing import List, Dict, Any, Optional
import requests
from dotenv import load_dotenv
import logging
from datetime import datetime
import json

load_dotenv()

class LogAnalyzer:
    def __init__(self):
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY", "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")
        self.huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.openrouter_model = os.getenv("OPENROUTER_MODEL", "deepseek/deepseek-r1-0528:free")
        self.huggingface_model = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.1")
        
        # Model configurations
        self.model_configs = {
            "deepseek/deepseek-r1-0528:free": {
                "provider": "openrouter",
                "endpoint": "https://openrouter.ai/api/v1/chat/completions",
                "headers": {
                    "Authorization": f"Bearer {self.openrouter_api_key}",
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "Linux Log Analyzer AI",
                    "Content-Type": "application/json"
                }
            },
            "mistralai/Mistral-7B-Instruct-v0.1": {
                "provider": "huggingface",
                "endpoint": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
            }
        }
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def preprocess_logs(self, log_text: str) -> str:
        """Preprocess log text for better analysis."""
        # Remove empty lines and normalize whitespace
        lines = [line.strip() for line in log_text.split('\n') if line.strip()]
        return '\n'.join(lines)

    def analyze_logs(self, log_text: str, model: str = None) -> Dict[str, Any]:
        """Analyze logs using the specified model."""
        if not model:
            model = self.openrouter_model

        if model not in self.model_configs:
            return {"error": f"Model {model} not supported"}

        config = self.model_configs[model]
        
        if config["provider"] == "openrouter":
            return self._analyze_with_openrouter(log_text)
        elif config["provider"] == "huggingface":
            return self._analyze_with_huggingface(log_text, model)
        else:
            return {"error": f"Provider {config['provider']} not supported"}

    def _analyze_with_openrouter(self, log_text: str) -> Dict[str, Any]:
        """Analyze logs using OpenRouter API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "HTTP-Referer": "https://github.com/yourusername/alert-triage-agent",
                "X-Title": "Alert Triage Agent",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "deepseek/deepseek-r1-0528:free",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a log analysis expert. Analyze the provided log and return a JSON response with the following structure: {\"summary\": \"brief summary\", \"issues\": [{\"description\": \"issue description\", \"severity\": \"severity level\", \"recommendation\": \"recommendation text\", \"command\": \"command to fix\", \"security_implication\": \"security impact\"}]}"
                    },
                    {
                        "role": "user",
                        "content": log_text
                    }
                ]
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                if "choices" in result and len(result["choices"]) > 0:
                    content = result["choices"][0]["message"]["content"]
                    return self._parse_analysis(content)
                else:
                    self.logger.error("Invalid response format from OpenRouter")
                    return {"error": "Invalid response format"}
            else:
                self.logger.error(f"OpenRouter API error: {response.text}")
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            self.logger.error(f"Error in OpenRouter analysis: {str(e)}")
            return {"error": str(e)}

    def _analyze_with_huggingface(self, log_text: str, model: str) -> Dict[str, Any]:
        """Analyze logs using HuggingFace API."""
        try:
            if not self.huggingface_api_key:
                return {"error": "HuggingFace API key not configured"}

            config = self.model_configs[model]
            headers = {"Authorization": f"Bearer {self.huggingface_api_key}"}
            
            prompt = f"""Analyze the following Linux system logs and provide:
1. A brief summary of the log content
2. Any issues or errors found, including:
   - Description
   - Severity (High/Medium/Low)
   - Recommendation
   - Command to fix (if applicable)
   - Security implication

Logs:
{log_text}

Format the response as JSON with the following structure:
{{
    "summary": "brief summary",
    "issues": [
        {{
            "description": "issue description",
            "severity": "High/Medium/Low",
            "recommendation": "how to fix",
            "command": "command to run",
            "security_implication": "security impact"
        }}
    ]
}}"""

            response = requests.post(
                config["endpoint"],
                headers=headers,
                json={"inputs": prompt}
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_analysis(result[0]["generated_text"])
            else:
                self.logger.error(f"HuggingFace API error: {response.text}")
                return {"error": f"HuggingFace API error: {response.text}"}
                
        except Exception as e:
            self.logger.error(f"Error in HuggingFace analysis: {str(e)}")
            return {"error": str(e)}

    def _parse_analysis(self, response_text: str) -> Dict[str, Any]:
        """Parse the analysis response into a structured format."""
        try:
            # Extract JSON from the response
            json_str = response_text[response_text.find("{"):response_text.rfind("}")+1]
            result = json.loads(json_str)
            
            # Validate the structure
            if not isinstance(result, dict) or "summary" not in result or "issues" not in result:
                return {"error": "Invalid response format"}
            
            # Validate and normalize issues
            normalized_issues = []
            for issue in result["issues"]:
                # Handle both old and new field names
                normalized_issue = {
                    "description": issue.get("description", ""),
                    "severity": issue.get("severity", "Medium"),
                    "recommendation": issue.get("recommendation") or issue.get("recommendations", [""])[0],
                    "command": issue.get("command") or issue.get("commands", [""])[0],
                    "security_implication": issue.get("security_implication") or issue.get("security_implications", [""])[0]
                }
                normalized_issues.append(normalized_issue)
            
            return {
                "summary": result["summary"],
                "issues": normalized_issues,
                "timestamp": datetime.now().isoformat()
            }
            
        except json.JSONDecodeError:
            self.logger.error("Failed to parse JSON response")
            return {"error": "Failed to parse analysis response"}
        except Exception as e:
            self.logger.error(f"Error parsing analysis: {str(e)}")
            return {"error": str(e)}

    def _determine_severity(self, log_line: str) -> str:
        """Determine severity based on common log patterns."""
        log_line = log_line.lower()
        if "failed password for user" in log_line or "possible syn flooding" in log_line:
            return "high"
        if "cpu temperature above threshold" in log_line or "out of memory" in log_line or "warning" in log_line:
            return "medium"
        if "failed to start" in log_line or "address already in use" in log_line or "killed process" in log_line:
            return "medium"
        return "low" 