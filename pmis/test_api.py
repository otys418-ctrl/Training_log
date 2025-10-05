"""
Quick API test script
"""
import requests
import time
import subprocess
import signal
import os

def test_api():
    # Start the server in background
    print("Starting FastAPI server...")
    server_process = subprocess.Popen(
        ["python3", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        # Test health check
        print("\nTesting health check endpoint...")
        response = requests.get("http://localhost:8000/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        # Test API documentation
        print("\nTesting API docs endpoint...")
        response = requests.get("http://localhost:8000/docs")
        print(f"Docs Status: {response.status_code}")
        
        print("\n✅ API is running successfully!")
        print("\nAvailable endpoints:")
        print("  - GET  /                          - Health check")
        print("  - POST /api/v1/plans/upload       - Upload training plan PDF")
        print("  - GET  /api/v1/plans/{user_id}    - Get full training plan")
        print("  - GET  /api/v1/plans/{user_id}/{day} - Get daily workout")
        print("  - DELETE /api/v1/plans/{user_id}  - Delete training plan")
        print("\nAPI Documentation: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"\n❌ Error testing API: {e}")
    finally:
        # Stop the server
        print("\nStopping server...")
        os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
        server_process.wait()

if __name__ == "__main__":
    test_api()
