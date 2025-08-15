# Chief Investigators Visualizer

This HTML visualizer provides an interactive way to explore the `ci_short_search_results.json` data.

## Quick Start

### Option 1: Using the Python Server (Recommended)
```bash
python3 serve_visualizer.py
```
This will:
- Start a local HTTP server on port 8000
- Automatically open the visualizer in your browser
- Avoid CORS issues when loading the JSON file

### Option 2: Manual HTTP Server
```bash
python3 -m http.server 8000
```
Then open: http://localhost:8000/visualizer.html

### Option 3: Simple File Opening (May not work due to CORS)
```bash
open visualizer.html
```

## Features

- **Statistics Dashboard**: View gender distribution and totals
- **Search**: Search across names, affiliations, research areas, and summaries
- **Filtering**: Filter by gender and confidence level
- **Responsive Design**: Works on desktop and mobile
- **Interactive Cards**: Expandable summaries and detailed information

## Troubleshooting

### "Error loading data" message
This typically happens when opening the HTML file directly in a browser due to CORS restrictions. Use Option 1 or 2 above to serve the files via HTTP.

### Files not found
Make sure both `visualizer.html` and `ci_short_search_results.json` are in the same directory.

### Port already in use
If port 8000 is busy, the server script will automatically try port 8001, 8002, etc.

## File Structure
```
academic-gender-search/
├── visualizer.html                 # Main HTML visualizer
├── ci_short_search_results.json   # Data file (required)
├── serve_visualizer.py            # Python server script
└── README_visualizer.md           # This file
```
