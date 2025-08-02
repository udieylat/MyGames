#!/usr/bin/env python3
"""
Simple HTTP server for the Magic Ball Game frontend.
Run this script to start a local server on port 8000.
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# Change to the frontend directory
os.chdir(Path(__file__).parent)

PORT = 8000

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers for development
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    try:
        with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
            print(f"Server started at http://localhost:{PORT}")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"Port {PORT} is already in use. Please try a different port.")
        else:
            print(f"Error starting server: {e}")

if __name__ == "__main__":
    main() 