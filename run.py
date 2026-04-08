import subprocess
import time
import sys
import os

def run():
    print("Starting FastAPI Backend...")
    # Add the current directory to python path for backend
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.dirname(os.path.abspath(__file__))
    
    backend = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"],
        env=env
    )
    
    time.sleep(2) # Give backend time to start
    
    print("Starting Streamlit Frontend...")
    frontend = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "frontend/app.py"]
    )
    
    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend.terminate()
        frontend.terminate()

if __name__ == "__main__":
    run()
