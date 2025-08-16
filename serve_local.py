#!/usr/bin/env python3
"""
Simple HTTP server to serve the academic gender search visualizer locally.
Run this script and then open http://localhost:8000/visualizer.html in your browser.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

def main():
    # Change to the directory containing this script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    PORT = 8000
    
    # Check if ci_short_search_results.json exists
    if not os.path.exists('ci_short_search_results.json'):
        print("❌ Error: ci_short_search_results.json not found!")
        print("Make sure you're running this script from the project directory.")
        sys.exit(1)
    
    # Check if visualizer.html exists
    if not os.path.exists('visualizer.html'):
        print("❌ Error: visualizer.html not found!")
        print("Make sure you're running this script from the project directory.")
        sys.exit(1)
    
    print(f"🚀 Starting local server on port {PORT}...")
    print(f"📊 Visualizer will be available at: http://localhost:{PORT}/visualizer.html")
    print(f"🏠 Index page will be available at: http://localhost:{PORT}/index.html")
    print("Press Ctrl+C to stop the server")
    
    try:
        with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
            print(f"✅ Server started successfully!")
            print(f"🌐 Opening browser...")
            
            # Automatically open the browser
            try:
                webbrowser.open(f'http://localhost:{PORT}/visualizer.html')
            except:
                print("Could not automatically open browser. Please manually visit the URL above.")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user.")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
