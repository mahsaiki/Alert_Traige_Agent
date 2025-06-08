import subprocess
import sys
import os
import time
from pathlib import Path

def run_backend():
    """Start the FastAPI backend server."""
    backend_cmd = [
        "uvicorn",
        "app.main:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
    ]
    return subprocess.Popen(backend_cmd)

def run_frontend():
    """Start the Streamlit frontend server."""
    frontend_cmd = [
        "streamlit",
        "run",
        "app/frontend/app.py",
        "--server.port=8501",
        "--server.address=localhost"
    ]
    return subprocess.Popen(frontend_cmd)

def main():
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print("Starting Alert Triage Agent...")
    
    # Start backend
    print("\nStarting backend server...")
    backend_process = run_backend()
    time.sleep(2)  # Wait for backend to start
    
    # Start frontend
    print("\nStarting frontend server...")
    frontend_process = run_frontend()
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("Servers stopped.")

if __name__ == "__main__":
    main() 