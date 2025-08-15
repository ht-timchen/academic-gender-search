#!/usr/bin/env python3
import json
import time
import os
from typing import Dict, List
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def analyze_ci_profile_with_search_model(name: str, affiliations: List[str]) -> Dict:
    """
    Analyze a CI profile using OpenAI's search-enabled models
    """
    
    prompt = f"""
    Search the web for information about academic researcher "{name}" who is affiliated with {', '.join(affiliations)}.
    
    I need you to find REAL, current information about this person including:
    1. Their research areas and specializations
    2. Recent publications or achievements
    3. Academic background and career highlights
    
    Based on your web search findings, provide a JSON response with:
    - "gender": "male", "female", or "unknown" (based on name analysis)
    - "summary": 2-3 sentence summary based on ACTUAL web search results (be honest if you find nothing)
    - "confidence": "high", "medium", or "low" for gender identification
    - "research_areas": List of 2-3 main research areas found through web search (or ["Unknown"] if none found)
    - "web_sources_found": Number of relevant web sources you actually found (0-5)
    - "search_successful": true if you found specific information about this person, false if no relevant results
    - "search_notes": Brief note about what you found or didn't find
    
    IMPORTANT: 
    - Only report information you actually found through web search
    - Don't make up research areas or achievements
    - Be honest about what you can and cannot find
    - If you find no specific information, say so clearly
    
    Return ONLY valid JSON, no other text.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-search-preview",  # Using search-enabled model
            messages=[
                {"role": "system", "content": "You are an academic profile analyzer with web search capabilities. Always be honest about what you find vs. what you don't find. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400
        )
        
        result_text = response.choices[0].message.content.strip()
        
        # Try to parse JSON
        try:
            result = json.loads(result_text)
            return result
        except json.JSONDecodeError:
            # Try to extract JSON from the response
            if '{' in result_text and '}' in result_text:
                start = result_text.find('{')
                end = result_text.rfind('}') + 1
                try:
                    result = json.loads(result_text[start:end])
                    return result
                except json.JSONDecodeError:
                    pass
            
            # If we can't parse JSON, return an error result
            return {
                "gender": "unknown",
                "summary": f"Response parsing failed. Raw response: {result_text[:100]}...",
                "confidence": "low",
                "research_areas": ["Unknown"],
                "web_sources_found": 0,
                "search_successful": False,
                "search_notes": "JSON parsing failed"
            }
        
    except Exception as e:
        print(f"Error with search model for {name}: {e}")
        return {
            "gender": "unknown",
            "summary": f"Academic researcher at {', '.join(affiliations)}. Search model failed.",
            "confidence": "low",
            "research_areas": ["Unknown"],
            "web_sources_found": 0,
            "search_successful": False,
            "search_notes": f"API error: {str(e)}"
        }

def load_cache(cache_file: str) -> Dict:
    """Load existing cache if it exists"""
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
                print(f"Loaded cache with {len(cache_data.get('results', []))} existing results")
                return cache_data
        except Exception as e:
            print(f"Error loading cache: {e}")
    
    return {"total_analyzed": 0, "results": []}

def save_cache(cache_file: str, data: Dict):
    """Save current progress to cache"""
    try:
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Progress saved to cache ({len(data['results'])} results)")
    except Exception as e:
        print(f"Error saving cache: {e}")

def get_processed_names(cache_data: Dict) -> set:
    """Get set of already processed names from cache"""
    return {result['name'] for result in cache_data.get('results', [])}

def process_cis_with_search_model(input_file: str, output_file: str, cache_file: str = "ci_search_model_cache.json"):
    """Process all CIs with search-enabled OpenAI models"""
    
    # Load input data
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Handle different input formats
    if isinstance(data, list):
        cis_list = data
    elif isinstance(data, dict) and 'unique_chief_investigators' in data:
        cis_list = data['unique_chief_investigators']
    else:
        raise ValueError("Unsupported data format")
    
    # Load existing cache
    cache_data = load_cache(cache_file)
    processed_names = get_processed_names(cache_data)
    results = cache_data.get('results', [])
    
    total_cis = len(cis_list)
    remaining_cis = [ci for ci in cis_list if ci['name'] not in processed_names]
    
    print(f"Total CIs: {total_cis}")
    print(f"Already processed: {len(processed_names)}")
    print(f"Remaining to process: {len(remaining_cis)}")
    
    if not remaining_cis:
        print("All CIs already processed!")
        output_data = {"total_analyzed": len(results), "results": results}
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        return
    
    print(f"Processing {len(remaining_cis)} remaining CIs with search-enabled model (gpt-4o-mini-search-preview)...")
    
    for i, ci in enumerate(remaining_cis, 1):
        print(f"Processing {i}/{len(remaining_cis)}: {ci['name']}")
        
        # Analyze with search-enabled model
        analysis = analyze_ci_profile_with_search_model(ci['name'], ci['affiliations'])
        
        # Create result entry
        result_entry = {
            "name": ci['name'],
            "affiliations": ci['affiliations'],
            "gender": analysis.get('gender', 'unknown'),
            "summary": analysis.get('summary', ''),
            "confidence": analysis.get('confidence', 'low'),
            "research_areas": analysis.get('research_areas', []),
            "web_sources_found": analysis.get('web_sources_found', 0),
            "search_successful": analysis.get('search_successful', False),
            "search_notes": analysis.get('search_notes', '')
        }
        
        results.append(result_entry)
        
        # Save progress frequently
        cache_data = {"total_analyzed": len(results), "results": results}
        save_cache(cache_file, cache_data)
        
        # Also save to final output
        output_data = {"total_analyzed": len(results), "results": results}
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        # Rate limiting
        time.sleep(2)
    
    print(f"\nAnalysis complete! Results saved to {output_file}")
    
    # Print statistics
    gender_counts = {}
    successful_searches = 0
    total_sources = 0
    
    for result in results:
        gender = result['gender']
        gender_counts[gender] = gender_counts.get(gender, 0) + 1
        if result.get('search_successful'):
            successful_searches += 1
        total_sources += result.get('web_sources_found', 0)
    
    print("\nGender Distribution:")
    for gender, count in gender_counts.items():
        percentage = (count / len(results)) * 100
        print(f"  {gender}: {count} ({percentage:.1f}%)")
    
    print(f"\nWeb Search Statistics:")
    print(f"  Successful searches: {successful_searches}/{len(results)} ({successful_searches/len(results)*100:.1f}%)")
    print(f"  Total web sources found: {total_sources}")
    print(f"  Average sources per CI: {total_sources/len(results):.1f}")
    
    # Clean up cache after completion
    if os.path.exists(cache_file):
        os.remove(cache_file)
        print(f"Cache file {cache_file} cleaned up")

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key in a .env file or environment variable")
        exit(1)
    
    # Process CIs with search-enabled model
    process_cis_with_search_model('ci_short.json', 'ci_short_search_results.json', 'ci_short_search_cache.json')
