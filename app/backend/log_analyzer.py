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
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        self.huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.openrouter_model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-2")
        self.huggingface_model = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.1")
        
        # Model configurations
        self.model_configs = {
            "anthropic/claude-2": {
                "provider": "openrouter",
                "endpoint": "https://openrouter.ai/api/v1/chat/completions"
            },
            "mistralai/Mistral-7B-Instruct-v0.1": {
                "provider": "huggingface",
                "endpoint": "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
            },
            "deepseek/deepseek-chat-v3-0324": {
                "provider": "openrouter",
                "endpoint": "https://openrouter.ai/api/v1/chat/completions"
            },
            "deepseek/deepseek-r1-0528": {
                "provider": "openrouter",
                "endpoint": "https://openrouter.ai/api/v1/chat/completions"
            },
            "google/gemini-2.0-flash-exp": {
                "provider": "openrouter",
                "endpoint": "https://openrouter.ai/api/v1/chat/completions"
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

    def analyze_logs(self, log_text: str, model: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze logs using the specified AI model.
        
        Args:
            log_text (str): The log text to analyze
            model (str, optional): The name of the model to use. If not specified,
                                 will use the default model from environment variables.
        
        Returns:
            Dict[str, Any]: Analysis results including summary and issues found
        """
        try:
            # Determine which model to use
            if model and model in self.model_configs:
                model_config = self.model_configs[model]
            else:
                # Use default model based on available API keys
                if self.openrouter_api_key:
                    model = self.openrouter_model
                    model_config = self.model_configs[model]
                elif self.huggingface_api_key:
                    model = self.huggingface_model
                    model_config = self.model_configs[model]
                else:
                    raise ValueError("No API keys configured for any model")

            # Check if we have the required API key
            if model_config["provider"] == "openrouter" and not self.openrouter_api_key:
                raise ValueError("OpenRouter API key not configured")
            elif model_config["provider"] == "huggingface" and not self.huggingface_api_key:
                raise ValueError("HuggingFace API key not configured")

            # Analyze using the appropriate provider
            if model_config["provider"] == "openrouter":
                return self.analyze_with_openrouter(log_text, model)
            else:
                return self.analyze_with_huggingface(log_text, model)

        except Exception as e:
            self.logger.error(f"Error analyzing logs: {str(e)}")
            return {
                "error": str(e),
                "summary": "Failed to analyze logs",
                "issues": []
            }

    def analyze_with_openrouter(self, log_text: str, model: str) -> Dict[str, Any]:
        """Analyze logs using OpenRouter API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a Linux log analysis expert. Analyze the provided logs and identify potential issues, security concerns, and performance problems. Provide a detailed analysis with specific recommendations."
                    },
                    {
                        "role": "user",
                        "content": f"Please analyze these Linux system logs and provide a detailed analysis:\n\n{log_text}"
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
                analysis = result["choices"][0]["message"]["content"]
                
                # Parse the analysis into a structured format
                return self._parse_analysis(analysis)
            else:
                raise Exception(f"OpenRouter API error: {response.text}")
                
        except Exception as e:
            self.logger.error(f"Error in OpenRouter analysis: {str(e)}")
            raise

    def analyze_with_huggingface(self, log_text: str, model: str) -> Dict[str, Any]:
        """Analyze logs using HuggingFace API."""
        try:
            headers = {
                "Authorization": f"Bearer {self.huggingface_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "inputs": f"Please analyze these Linux system logs and provide a detailed analysis:\n\n{log_text}",
                "parameters": {
                    "max_length": 1000,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            response = requests.post(
                "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                analysis = result[0]["generated_text"]
                
                # Parse the analysis into a structured format
                return self._parse_analysis(analysis)
            else:
                raise Exception(f"HuggingFace API error: {response.text}")
                
        except Exception as e:
            self.logger.error(f"Error in HuggingFace analysis: {str(e)}")
            raise

    def _parse_analysis(self, analysis) -> Dict[str, Any]:
        """Parse the AI model's analysis into a structured format."""
        try:
            # If analysis is a dict (e.g., from test mocks), extract 'content'
            if isinstance(analysis, dict):
                if 'content' in analysis:
                    analysis = analysis['content']
                else:
                    # If dict but no 'content', treat as error
                    raise ValueError("Analysis dict missing 'content' field")

            # If analysis is a JSON string, parse it
            if isinstance(analysis, str):
                try:
                    parsed = json.loads(analysis)
                    if isinstance(parsed, dict) and 'summary' in parsed and 'issues' in parsed:
                        parsed['timestamp'] = datetime.now().isoformat()
                        return parsed
                except Exception:
                    pass  # Not a JSON string, fall back to text parsing

            # Fallback: treat as plain text and use split-based logic
            sections = analysis.split("\n\n") if isinstance(analysis, str) else []
            summary = sections[0] if sections else "No summary available"
            issues = []
            current_issue = {}
            for section in sections[1:]:
                if "Issue:" in section:
                    if current_issue:
                        issues.append(current_issue)
                    current_issue = {
                        "description": section.split("Issue:")[1].strip(),
                        "severity": "Medium",  # Default severity
                        "recommendations": [],
                        "commands": [],
                        "security_implications": []
                    }
                elif "Severity:" in section:
                    current_issue["severity"] = section.split("Severity:")[1].strip()
                elif "Recommendation:" in section:
                    current_issue["recommendations"].append(section.split("Recommendation:")[1].strip())
                elif "Command to fix:" in section:
                    current_issue["commands"].append(section.split("Command to fix:")[1].strip())
                elif "Security implications:" in section:
                    current_issue["security_implications"].append(section.split("Security implications:")[1].strip())
            if current_issue:
                issues.append(current_issue)
            return {
                "summary": summary,
                "issues": issues,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error parsing analysis: {str(e)}")
            return {
                "summary": "Error parsing analysis",
                "issues": [],
                "timestamp": datetime.now().isoformat()
            }

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