# WORK IN PROGRESS

## Academic Gender Search Analysis

An interactive web application for analyzing gender distribution among chief investigators in academic research.

## 🚀 Live Demo 

Visit the live application: [https://ht-timchen.github.io/academic-gender-search](https://ht-timchen.github.io/academic-gender-search)

## 📊 Overview

This project provides a comprehensive analysis of **2,679 Chief Investigators** with 3+ Discovery Projects using a three-tier methodology:

- **Tier 1**: Web search analysis (74.8% - 2,004 researchers)
- **Tier 2**: Name-based AI predictions (18.4% - 493 researchers) 
- **Tier 3**: Manual review system (6.8% - 182 researchers)

### Final Results:
- **Male**: 1,906 (71.1%)
- **Female**: 591 (22.1%) 
- **Unknown**: 182 (6.8%)

### Features:
- **Gender distribution analysis** with transparent confidence levels
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

## 🔬 Three-Tier Methodology

### Tier 1: Web Search Analysis (74.8%)
- **Tool**: OpenAI GPT-4o-mini-search-preview with web search capabilities
- **Process**: Searches academic profiles, publications, institutional pages
- **Output**: High-confidence gender identification with research areas
- **Cost**: AUD $72.11 for 2,679 researchers

### Tier 2: Name-Based AI Analysis (18.4%) 
- **Tool**: OpenAI GPT-4o-mini (no web search)
- **Process**: Analyzes name patterns and linguistic origins
- **Output**: Speculative predictions clearly marked in metadata
- **Cost**: ~AUD $14.50 for 675 researchers (493 successful predictions)

### Tier 3: Manual Review System (6.8%)
- **Process**: Community-driven corrections via GitHub Issues
- **Target**: Remaining 182 researchers + any misclassifications
- **Transparency**: Full audit trail and correction history

## 📁 Project Structure

```
academic-gender-search/
├── index.html                         # Landing page with methodology
├── visualizer.html                    # Main interactive application
├── ci_gender.json                     # Final merged dataset (Tier 1+2)
├── ci_short_search_results.json       # Tier 1 web search results
├── ci_name_based_gender_analysis.json # Tier 2 name analysis results
├── ci_gender_analyzer_v3.py           # Tier 1 analyzer (web search)
├── ci_name_based_gender_analyzer.py   # Tier 2 analyzer (name-based)
├── serve_local.py                     # Local development server
├── .github/workflows/deploy.yml       # GitHub Pages deployment
└── README.md                          # This file
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

The final dataset (`ci_gender.json`) includes comprehensive metadata:

```json
{
  "total_analyzed": 2679,
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
      "search_notes": "Tier 1 web search notes or Tier 2 name analysis disclaimer",
      "name_analysis": {
        "method": "name_pattern_analysis",
        "original_gender": "unknown", 
        "name_based_gender": "male",
        "confidence": "high",
        "reasoning": "Common masculine name pattern",
        "disclaimer": "Speculative prediction based on name only"
      }
    }
  ]
}
```

### Key Fields:
- **Tier 1 data**: `web_sources_found`, `search_successful`, detailed `summary`
- **Tier 2 data**: `name_analysis` object with prediction metadata
- **All tiers**: Clear confidence indicators and transparency notes

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
