#!/usr/bin/env python3
import json
import os

def clean_api_error_entries(results_file, cache_file):
    """
    Remove entries with API errors from both results and cache files
    """
    
    # Load the results file
    print(f"Loading {results_file}...")
    with open(results_file, 'r') as f:
        data = json.load(f)
    
    original_count = len(data['results'])
    print(f"Original count: {original_count}")
    
    # Filter out entries with API errors
    clean_results = []
    removed_count = 0
    
    for result in data['results']:
        search_notes = result.get('search_notes', '')
        
        # Check for various API error patterns
        has_api_error = (
            'exceeded your current quota' in search_notes or
            'API error: Error code: 429' in search_notes or
            'insufficient_quota' in search_notes or
            'Search model failed' in result.get('summary', '') and 'API error' in search_notes
        )
        
        if has_api_error:
            removed_count += 1
            print(f"Removing entry with API error: {result['name']}")
        else:
            clean_results.append(result)
    
    # Update the data
    data['results'] = clean_results
    data['total_analyzed'] = len(clean_results)
    
    print(f"Removed {removed_count} entries with API errors")
    print(f"Clean count: {len(clean_results)}")
    
    # Save cleaned results
    print(f"Saving cleaned results to {results_file}...")
    with open(results_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Update cache file as well if it exists
    if os.path.exists(cache_file):
        print(f"Updating cache file {cache_file}...")
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    print("Cleanup complete!")
    return len(clean_results), removed_count

if __name__ == "__main__":
    results_file = "ci_short_search_results.json"
    cache_file = "ci_short_search_cache.json"
    
    clean_count, removed_count = clean_api_error_entries(results_file, cache_file)
    
    print(f"\nSummary:")
    print(f"  - Entries removed: {removed_count}")
    print(f"  - Clean entries remaining: {clean_count}")
    print(f"  - Ready to resume processing from entry {clean_count + 1}")