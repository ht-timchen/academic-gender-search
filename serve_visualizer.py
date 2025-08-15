#!/usr/bin/env python3
"""
Simple HTTP server to serve the HTML visualizer and JSON data.
This avoids CORS issues when loading local JSON files.
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

def serve_visualizer(port=8000):
    """Start a local HTTP server and open the visualizer in the browser."""
    
    # Change to the script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check if required files exist
    if not Path("visualizer.html").exists():
        print("Error: visualizer.html not found in current directory")
        return
    
    if not Path("ci_short_search_results.json").exists():
        print("Error: ci_short_search_results.json not found in current directory")
        return
    
    # Set up the server
    Handler = http.server.SimpleHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"Serving at http://localhost:{port}")
            print(f"Opening visualizer at http://localhost:{port}/visualizer.html")
            print("Press Ctrl+C to stop the server")
            
            # Open the visualizer in the default browser
            webbrowser.open(f"http://localhost:{port}/visualizer.html")
            
            # Start serving
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"Port {port} is already in use. Trying port {port + 1}")
            serve_visualizer(port + 1)
        else:
            print(f"Error starting server: {e}")

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8000.")
    
    serve_visualizer(port)
