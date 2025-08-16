#!/usr/bin/env python3
"""
Simple script to run name-based gender analysis on unknown gender researchers
"""

import json
import os
from ci_name_based_gender_analyzer import process_unknown_gender_researchers

def main():
    # Check if API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please set your OpenAI API key in a .env file or environment variable")
        exit(1)
    
    # Check if input file exists
    input_file = 'ci_short_search_results.json'
    if not os.path.exists(input_file):
        print(f"❌ Error: {input_file} not found!")
        print("Make sure you're running this script from the project directory.")
        exit(1)
    
    # Check how many unknown gender researchers we have
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    unknown_count = sum(1 for r in data['results'] if r.get('gender') == 'unknown')
    total_count = len(data['results'])
    
    print("🔍 Name-Based Gender Analysis")
    print("=" * 50)
    print(f"📊 Total researchers: {total_count}")
    print(f"❓ Unknown gender: {unknown_count}")
    print(f"💡 Will analyze: {unknown_count} names")
    print("=" * 50)
    
    if unknown_count == 0:
        print("✅ No researchers with unknown gender found!")
        return
    
    # Estimate cost and time
    estimated_cost = unknown_count * 0.0001  # Rough estimate for gpt-4o-mini
    estimated_time = unknown_count * 1.5  # 1.5 seconds per request including rate limiting
    
    print(f"⏱️  Estimated time: {estimated_time/60:.1f} minutes")
    print(f"💰 Estimated cost: ~${estimated_cost:.2f} USD")
    print("=" * 50)
    
    # Confirm before proceeding
    response = input("Proceed with name-based analysis? (y/n): ").lower().strip()
    if response != 'y' and response != 'yes':
        print("❌ Analysis cancelled.")
        return
    
    # Run the analysis
    output_file = 'ci_name_based_gender_analysis.json'
    
    print("\n🚀 Starting name-based gender analysis...")
    print("This will create detailed notes that these are speculative predictions.")
    
    try:
        process_unknown_gender_researchers(input_file, output_file)
        
        print("\n✅ Analysis complete!")
        print(f"📄 Results saved to: {output_file}")
        print("\n💡 Next steps:")
        print("1. Review the results in the JSON file")
        print("2. Run the full analyzer to merge results if satisfied")
        print("3. Or adjust the analysis parameters and re-run")
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        print("Check your OpenAI API key and internet connection.")

if __name__ == "__main__":
    main()
