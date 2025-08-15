# WORK IN PROGRESS

## Academic Gender Search Analysis

An interactive web application for analyzing gender distribution among chief investigators in academic research.

## 🚀 Live Demo 

Visit the live application: [https://ht-timchen.github.io/academic-gender-search](https://ht-timchen.github.io/academic-gender-search)

## 📊 Overview

This project provides a comprehensive analysis of 1,531 chief investigators, including:

- **Gender distribution analysis** with confidence levels
- **Institutional affiliations** and research areas
- **Interactive search and filtering** capabilities
- **Responsive design** for all devices

## ✨ Features

### 🔍 **Search & Filter**
- Real-time search across names, affiliations, and research areas
- Filter by gender (Male, Female, Unknown)
- Filter by confidence level (High, Medium, Low)

### 📈 **Statistics Dashboard**
- Live statistics showing gender distribution
- Total researcher count with breakdowns
- Visual indicators for data confidence

### 🎨 **Modern Interface**
- Clean, minimal design
- Color-coded badges for easy identification
- Expandable summaries for detailed information
- Mobile-responsive layout

### 📱 **Responsive Design**
- Works on desktop, tablet, and mobile
- Optimized for all screen sizes
- Touch-friendly interface

## 🛠️ Technical Stack

- **Frontend**: Pure HTML, CSS, JavaScript
- **Data**: JSON format with comprehensive researcher profiles
- **Deployment**: GitHub Pages (static hosting)
- **No dependencies**: Runs entirely in the browser

## 📁 Project Structure

```
academic-gender-search/
├── index.html                      # Landing page
├── visualizer.html                 # Main application
├── ci_short_search_results.json    # Research data
├── serve_visualizer.py             # Local development server
├── .github/workflows/deploy.yml    # GitHub Pages deployment
└── README.md                       # This file
```

## 🚀 Local Development

### Option 1: Python Server
```bash
python3 serve_visualizer.py
```

### Option 2: Simple HTTP Server
```bash
python3 -m http.server 8000
# Open http://localhost:8000
```

### Option 3: Direct File Opening
```bash
open visualizer.html
# Note: May have CORS issues with local JSON loading
```

## 📈 Data Format

The application uses JSON data with the following structure:

```json
{
  "total_analyzed": 1531,
  "results": [
    {
      "name": "Researcher Name",
      "affiliations": ["University Name"],
      "gender": "male|female|unknown",
      "summary": "Research background and details...",
      "confidence": "high|medium|low",
      "research_areas": ["Area 1", "Area 2"],
      "web_sources_found": 5,
      "search_successful": true,
      "search_notes": "Additional information..."
    }
  ]
}
```

## 🌐 Deployment

This project is automatically deployed to GitHub Pages when changes are pushed to the main branch.

### Manual Deployment Steps:

1. **Enable GitHub Pages** in repository settings
2. **Set source** to "GitHub Actions"
3. **Push changes** to main branch
4. **Workflow will automatically deploy** the site

### Custom Domain (Optional):

1. Add `CNAME` file with your domain
2. Configure DNS settings
3. Enable HTTPS in repository settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally using the development server
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for academic research transparency**
