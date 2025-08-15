#!/usr/bin/env python3
import json
import os

def clean_error_entries(input_file: str, output_file: str = None):
    """
    Remove entries with error messages and keep only successfully processed ones
    """
    if output_file is None:
        output_file = input_file
    
    try:
        # Load the data
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        original_count = len(data.get('results', []))
        print(f"Original entries: {original_count}")
        
        # Filter out entries with error messages
        clean_results = []
        error_count = 0
        
        for entry in data.get('results', []):
            summary = entry.get('summary', '')
            search_notes = entry.get('search_notes', '')
            
            # Check if entry contains error messages
            has_error = (
                'API error:' in search_notes or
                'Error code:' in search_notes or
                'insufficient_quota' in summary or
                'API error:' in summary or
                'Search model failed' in summary
            )
            
            if not has_error:
                clean_results.append(entry)
            else:
                error_count += 1
                print(f"Removing error entry: {entry.get('name', 'Unknown')}")
        
        # Update the data
        data['results'] = clean_results
        data['total_analyzed'] = len(clean_results)
        
        # Save the cleaned data
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nCleaning complete:")
        print(f"  Original entries: {original_count}")
        print(f"  Error entries removed: {error_count}")
        print(f"  Clean entries remaining: {len(clean_results)}")
        print(f"  Cleaned data saved to: {output_file}")
        
        # Show statistics of clean data
        if clean_results:
            successful_searches = sum(1 for r in clean_results if r.get('search_successful', False))
            total_sources = sum(r.get('web_sources_found', 0) for r in clean_results)
            
            print(f"\nClean data statistics:")
            print(f"  Successful searches: {successful_searches}/{len(clean_results)} ({successful_searches/len(clean_results)*100:.1f}%)")
            print(f"  Total web sources: {total_sources}")
            print(f"  Average sources per CI: {total_sources/len(clean_results):.1f}")
            
            # Gender distribution
            gender_counts = {}
            for result in clean_results:
                gender = result.get('gender', 'unknown')
                gender_counts[gender] = gender_counts.get(gender, 0) + 1
            
            print(f"\nGender Distribution:")
            for gender, count in gender_counts.items():
                percentage = (count / len(clean_results)) * 100
                print(f"  {gender}: {count} ({percentage:.1f}%)")
        
        return len(clean_results)
        
    except Exception as e:
        print(f"Error cleaning entries: {e}")
        return 0

if __name__ == "__main__":
    # Clean the main results file
    results_file = 'ci_short_search_results.json'
    cache_file = 'ci_short_search_cache.json'
    
    if os.path.exists(results_file):
        print("Cleaning results file...")
        clean_count = clean_error_entries(results_file)
        
        # Also clean the cache file to match
        if os.path.exists(cache_file) and clean_count > 0:
            print(f"\nCleaning cache file to match...")
            clean_error_entries(cache_file)
    else:
        print(f"Results file {results_file} not found")


