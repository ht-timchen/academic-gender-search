# CI Gender Analyzer with OpenAI Web Search

An LLM agent that uses OpenAI API with built-in web search tool to analyze Chief Investigator profiles, identify gender, extract research information, and create comprehensive summaries.

## Features

- **OpenAI Web Search**: Uses OpenAI's built-in web search tool for academic profile information
- **Profile Extraction**: Extracts research areas, publications, and achievements from web results
- **Gender Identification**: Analyzes names to identify gender with confidence levels
- **Comprehensive Summaries**: Creates detailed 2-3 sentence summaries based on web data
- **Research Area Classification**: Identifies main research fields and specializations
- **Caching & Resume**: Saves progress frequently and can resume from interruptions

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up OpenAI API key:**
   Create a `.env` file in the project directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   
   Or set it as an environment variable:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

Run the analyzer on the test file:
```bash
python ci_gender_analyzer.py
```

### Caching & Resume Functionality

The script includes robust caching to handle interruptions:

- **Frequent Saves**: Progress is saved after each CI analysis
- **Resume Capability**: Can resume from where it left off if interrupted
- **Cache File**: Uses `ci_analysis_cache.json` for temporary storage
- **Auto Cleanup**: Cache file is automatically removed after successful completion

**Example of resumption:**
```bash
# If interrupted, just run again:
python ci_gender_analyzer.py
# Script will detect existing cache and resume from last processed CI
```

**Test caching functionality:**
```bash
python test_cache.py
# Creates a test cache to simulate interruption
```

## Input Format

The script expects a JSON file with the structure:
```json
{
  "unique_chief_investigators": [
    {
      "name": "Dr. Jane Smith",
      "affiliations": ["University A", "University B"]
    }
  ]
}
```

Or a direct array format:
```json
[
  {
    "name": "Dr. Jane Smith",
    "affiliations": ["University A", "University B"]
  }
]
```

## Output Format

The script generates `ci_analysis_results.json` with enhanced information:
```json
{
  "total_analyzed": 14,
  "results": [
    {
      "name": "Dr. Jane Smith",
      "affiliations": ["University A", "University B"],
      "gender": "female",
      "summary": "Leading researcher in computational biology with expertise in machine learning applications for genomic analysis. Has published extensively in Nature and Science journals.",
      "confidence": "high",
      "research_areas": ["Computational Biology", "Machine Learning", "Genomics"],
      "web_sources": 3
    }
  ]
}
```

## Enhanced Features

- **OpenAI Web Search**: Uses GPT-4o-mini with built-in web search tool for comprehensive profile analysis
- **Research Area Extraction**: Identifies 2-3 main research fields per researcher
- **Comprehensive Summaries**: 2-3 sentence summaries including research achievements
- **Source Tracking**: Counts number of web sources found for each profile
- **Rate Limiting**: 2-second delays between requests to respect API limits
- **Error Handling**: Graceful fallbacks for failed web searches or API calls
- **Caching System**: Frequent progress saves and resume capability

## Web Search Process

1. **Tool Integration**: Uses OpenAI's web_search tool in GPT-4o-mini
2. **Query Formation**: Automatically creates search queries for academic profiles
3. **Result Analysis**: LLM analyzes web search results for relevant information
4. **Profile Synthesis**: Combines web data with basic information for comprehensive profiles

## Cost Estimation

- Uses GPT-4o-mini with web search tool (~$0.015 per 1K tokens)
- Each CI analysis uses ~150-200 tokens (including web search)
- For 14 CIs: ~$0.03-0.04 total cost
- Web search is included in OpenAI API cost

## Performance

- **Processing Time**: ~2 seconds per CI (API call with web search)
- **Success Rate**: High for researchers with web presence
- **Data Quality**: Significantly enhanced with real research information
- **Model**: GPT-4o-mini for cost-effective analysis
- **Reliability**: Caching ensures no data loss on interruptions
