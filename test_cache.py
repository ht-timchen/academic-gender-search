#!/usr/bin/env python3
"""
Test script to demonstrate caching functionality
"""
import json
import os

def create_test_cache():
    """Create a test cache file to simulate interruption"""
    test_cache = {
        "total_analyzed": 3,
        "results": [
            {
                "name": "A/Prof Aaron Jex",
                "affiliations": ["The University of Sydney", "The University of Melbourne"],
                "gender": "male",
                "summary": "Test summary for Aaron Jex",
                "confidence": "high",
                "research_areas": ["Test Research Area"],
                "web_sources": 3
            },
            {
                "name": "A/Prof Aaron Oakley", 
                "affiliations": ["University of Wollongong"],
                "gender": "male",
                "summary": "Test summary for Aaron Oakley",
                "confidence": "high",
                "research_areas": ["Test Research Area"],
                "web_sources": 3
            },
            {
                "name": "A/Prof Abdullah Mamun",
                "affiliations": ["The University of Queensland"],
                "gender": "male", 
                "summary": "Test summary for Abdullah Mamun",
                "confidence": "high",
                "research_areas": ["Test Research Area"],
                "web_sources": 3
            }
        ]
    }
    
    with open('ci_analysis_cache.json', 'w') as f:
        json.dump(test_cache, f, indent=2)
    
    print("Test cache created with 3 processed CIs")

if __name__ == "__main__":
    print("Caching Test Script")
    print("1. Create test cache")
    print("2. Run main script to see resumption")
    
    choice = input("Enter choice (1 or 2): ")
    
    if choice == "1":
        create_test_cache()
        print("Test cache created. Now run the main script to see resumption.")
    elif choice == "2":
        print("Run: python ci_gender_analyzer.py")
    else:
        print("Invalid choice")


