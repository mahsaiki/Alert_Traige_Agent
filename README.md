# Linux Log Analyzer AI

A web-based Linux Log Analyzer that uses AI to analyze system logs and provide insights, recommendations, and security implications.

## Features

- File upload and text input for log analysis
- AI-powered log analysis using OpenRouter.ai or HuggingFace APIs
- Modern, responsive UI with Streamlit
- Color-coded severity indicators
- Expandable issue panels
- Ready-to-use shell commands
- Export analysis results in JSON and CSV formats
- Theme customization (light/dark mode)
- Analysis history tracking

## Prerequisites

- Python 3.8 or higher
- API key for either OpenRouter.ai or HuggingFace (or both)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd linux-log-analyzer-ai
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your API keys:
```
OPENROUTER_API_KEY=your_openrouter_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

## Running Tests

To run the test suite:

```bash
python scripts/run_tests.py
```

This will run all tests in the `tests` directory with detailed output.

## Running the Application

To start the application:

```bash
python scripts/run_app.py
```

The application will be available at `http://localhost:8501`

## Usage

1. Open your web browser and navigate to `http://localhost:8501`
2. Choose your preferred theme and AI model in the sidebar
3. Upload a log file or paste log text into the input area
4. Click "Analyze Logs" to process the logs
5. View the analysis results:
   - Summary of findings
   - Issues with severity indicators
   - Recommendations and commands
   - Security implications
6. Export results in JSON or CSV format if needed
7. View analysis history in the sidebar

## Configuration

The following environment variables can be configured in the `.env` file:

- `OPENROUTER_API_KEY`: Your OpenRouter.ai API key
- `HUGGINGFACE_API_KEY`: Your HuggingFace API key
- `OPENROUTER_MODEL`: Model to use with OpenRouter (default: "anthropic/claude-2")
- `HUGGINGFACE_MODEL`: Model to use with HuggingFace (default: "mistralai/Mistral-7B-Instruct-v0.1")

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
