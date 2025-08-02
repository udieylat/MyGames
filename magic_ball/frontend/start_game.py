#!/usr/bin/env python3
"""
Startup script for the Magic Ball Game web interface.
Installs dependencies and starts the Flask server.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required Python packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False
    return True

def start_server():
    """Start the Flask server"""
    print("Starting Magic Ball Game server...")
    print("Access the game at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")

def main():
    print("Magic Ball Game - Web Interface")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not Path("app.py").exists():
        print("Error: Please run this script from the frontend directory")
        return
    
    # Install dependencies
    if not install_requirements():
        return
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main() 