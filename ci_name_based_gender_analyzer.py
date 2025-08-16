#!/usr/bin/env python3
"""
Name-Based Gender Analyzer for Unknown Gender Cases

This script processes researchers with "unknown" gender from the main analysis
and uses GPT (without web search) to make educated guesses based on name patterns.
All predictions are clearly marked as speculative and based solely on name analysis.
"""

import json
import time
import os
from typing import Dict, List
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def analyze_name_for_gender(name: str) -> Dict:
    """
    Analyze a name using GPT (without web search) to make educated gender guess
    """
    
    prompt = f"""
    Analyze the name "{name}" and make your best educated guess about the person's gender based solely on the name.
    
    Consider:
    1. Common gender associations with given names
    2. Cultural and linguistic patterns
    3. Name variations and origins
    
    IMPORTANT: You do NOT have access to web search or any external information about this specific person.
    Base your analysis ONLY on the name itself and general naming patterns.
    
    Provide a JSON response with:
    - "gender": "male", "female", or "unknown" (your best guess based on name only)
    - "confidence": "high", "medium", or "low" (how confident you are in this name-based guess)
    - "reasoning": Brief explanation of why you made this guess
    - "name_origin": If recognizable, the likely cultural/linguistic origin of the name
    - "ambiguity_notes": Any notes about name ambiguity or uncertainty
    
    Be honest about uncertainty. If the name is genuinely ambiguous or you're unsure, 
    use "unknown" and explain why.
    
    Return ONLY valid JSON, no other text.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using standard model without web search
            messages=[
                {"role": "system", "content": "You are a name analysis expert. You analyze names for likely gender associations based on linguistic and cultural patterns. You do NOT have web search access and must base analysis purely on the name provided. Be honest about uncertainty."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.1  # Low temperature for more consistent analysis
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
                "confidence": "low",
                "reasoning": f"JSON parsing failed. Raw response: {result_text[:150]}...",
                "name_origin": "Unknown",
                "ambiguity_notes": "Analysis failed due to parsing error"
            }
        
    except Exception as e:
        print(f"Error analyzing name {name}: {e}")
        return {
            "gender": "unknown",
            "confidence": "low", 
            "reasoning": f"API error: {str(e)}",
            "name_origin": "Unknown",
            "ambiguity_notes": "Analysis failed due to API error"
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

def process_unknown_gender_researchers(input_file: str, output_file: str, cache_file: str = "name_analysis_cache.json"):
    """Process researchers with unknown gender using name-based analysis"""
    
    # Load input data
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Extract researchers with unknown gender
    all_researchers = data.get('results', [])
    unknown_gender_researchers = [r for r in all_researchers if r.get('gender') == 'unknown']
    
    print(f"Found {len(unknown_gender_researchers)} researchers with unknown gender")
    
    # Load existing cache
    cache_data = load_cache(cache_file)
    processed_names = get_processed_names(cache_data)
    results = cache_data.get('results', [])
    
    remaining_researchers = [r for r in unknown_gender_researchers if r['name'] not in processed_names]
    
    print(f"Already processed: {len(processed_names)}")
    print(f"Remaining to process: {len(remaining_researchers)}")
    
    if not remaining_researchers:
        print("All unknown gender researchers already processed!")
        output_data = {"total_analyzed": len(results), "results": results}
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        return
    
    print(f"Processing {len(remaining_researchers)} researchers with name-based gender analysis...")
    
    for i, researcher in enumerate(remaining_researchers, 1):
        print(f"Processing {i}/{len(remaining_researchers)}: {researcher['name']}")
        
        # Analyze name for gender
        name_analysis = analyze_name_for_gender(researcher['name'])
        
        # Create enhanced result entry
        result_entry = {
            "name": researcher['name'],
            "affiliations": researcher['affiliations'],
            "original_gender": researcher['gender'],  # Keep track of original classification
            "original_summary": researcher.get('summary', ''),
            "original_search_notes": researcher.get('search_notes', ''),
            
            # Name-based analysis results
            "name_based_gender": name_analysis.get('gender', 'unknown'),
            "name_analysis_confidence": name_analysis.get('confidence', 'low'),
            "name_reasoning": name_analysis.get('reasoning', ''),
            "name_origin": name_analysis.get('name_origin', 'Unknown'),
            "ambiguity_notes": name_analysis.get('ambiguity_notes', ''),
            
            # Updated search notes with clear disclaimer
            "updated_search_notes": f"{researcher.get('search_notes', '')} | NAME-BASED GENDER ANALYSIS: No clear evidence found on websites during original search. Gender prediction '{name_analysis.get('gender', 'unknown')}' is based solely on name pattern analysis using AI, not on verified information about this specific person. Confidence: {name_analysis.get('confidence', 'low')}. Reasoning: {name_analysis.get('reasoning', 'No reasoning provided')}",
            
            # Analysis metadata
            "analysis_method": "name_pattern_only",
            "analysis_date": time.strftime("%Y-%m-%d"),
            "disclaimer": "This gender classification is speculative and based only on name patterns, not verified information about the individual."
        }
        
        results.append(result_entry)
        
        # Save progress frequently
        cache_data = {"total_analyzed": len(results), "results": results}
        save_cache(cache_file, cache_data)
        
        # Also save to final output
        output_data = {"total_analyzed": len(results), "results": results}
        with open(output_file, 'w') as f:
            json.dump(output_data, f, indent=2)
        
        # Rate limiting to be respectful to API
        time.sleep(1)
    
    print(f"\nName-based analysis complete! Results saved to {output_file}")
    
    # Print statistics
    gender_counts = {}
    confidence_counts = {}
    
    for result in results:
        gender = result['name_based_gender']
        confidence = result['name_analysis_confidence']
        
        gender_counts[gender] = gender_counts.get(gender, 0) + 1
        confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1
    
    print("\nName-Based Gender Predictions:")
    for gender, count in gender_counts.items():
        percentage = (count / len(results)) * 100
        print(f"  {gender}: {count} ({percentage:.1f}%)")
    
    print("\nConfidence Levels:")
    for confidence, count in confidence_counts.items():
        percentage = (count / len(results)) * 100
        print(f"  {confidence}: {count} ({percentage:.1f}%)")
    
    print(f"\nTotal researchers analyzed: {len(results)}")
    print(f"Average processing time: ~{len(results)} seconds (1 sec per researcher)")
    
    # Clean up cache after completion
    if os.path.exists(cache_file):
        os.remove(cache_file)
        print(f"Cache file {cache_file} cleaned up")

def merge_results_back_to_main(original_file: str, name_analysis_file: str, output_file: str):
    """
    Merge the name-based analysis results back into the main dataset
    """
    print("Merging name-based analysis back into main dataset...")
    
    # Load original data
    with open(original_file, 'r') as f:
        original_data = json.load(f)
    
    # Load name analysis results
    with open(name_analysis_file, 'r') as f:
        name_analysis_data = json.load(f)
    
    # Create lookup for name analysis results
    name_analysis_lookup = {result['name']: result for result in name_analysis_data['results']}
    
    # Update original results
    updated_results = []
    updates_made = 0
    
    for researcher in original_data['results']:
        if researcher['name'] in name_analysis_lookup:
            # This researcher had name-based analysis
            analysis = name_analysis_lookup[researcher['name']]
            
            # Update the researcher data
            updated_researcher = researcher.copy()
            
            # Only update if name-based analysis provided a gender prediction
            if analysis['name_based_gender'] != 'unknown':
                updated_researcher['gender'] = analysis['name_based_gender']
                updated_researcher['confidence'] = analysis['name_analysis_confidence']
                updates_made += 1
            
            # Always update search notes to include the disclaimer
            updated_researcher['search_notes'] = analysis['updated_search_notes']
            
            # Add name analysis metadata
            updated_researcher['name_analysis'] = {
                "method": "name_pattern_analysis",
                "original_gender": analysis['original_gender'],
                "name_based_gender": analysis['name_based_gender'],
                "confidence": analysis['name_analysis_confidence'],
                "reasoning": analysis['name_reasoning'],
                "name_origin": analysis['name_origin'],
                "disclaimer": analysis['disclaimer']
            }
            
            updated_results.append(updated_researcher)
        else:
            # No name-based analysis for this researcher
            updated_results.append(researcher)
    
    # Save merged results
    merged_data = {
        "total_analyzed": len(updated_results),
        "results": updated_results
    }
    
    with open(output_file, 'w') as f:
        json.dump(merged_data, f, indent=2)
    
    print(f"Merge complete! {updates_made} researchers updated with name-based gender predictions")
    print(f"Merged results saved to {output_file}")

if __name__ == "__main__":
    # Check if API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key in a .env file or environment variable")
        exit(1)
    
    # Process unknown gender researchers with name-based analysis
    input_file = 'ci_short_search_results.json'
    analysis_output = 'ci_name_based_gender_analysis.json'
    merged_output = 'ci_short_search_results_with_name_analysis.json'
    
    print("=" * 60)
    print("CI Name-Based Gender Analyzer")
    print("=" * 60)
    print("This tool analyzes researchers with 'unknown' gender using")
    print("name pattern analysis only (no web search).")
    print("All predictions are clearly marked as speculative.")
    print("=" * 60)
    
    # Step 1: Analyze unknown gender researchers
    process_unknown_gender_researchers(input_file, analysis_output)
    
    print("\n" + "=" * 60)
    print("Analysis complete! Now merging results...")
    print("=" * 60)
    
    # Step 2: Merge results back into main dataset
    merge_results_back_to_main(input_file, analysis_output, merged_output)
    
    print("\n" + "=" * 60)
    print("✅ Name-based gender analysis complete!")
    print(f"📊 Original data: {input_file}")
    print(f"🔍 Name analysis: {analysis_output}")
    print(f"🔄 Merged results: {merged_output}")
    print("=" * 60)
