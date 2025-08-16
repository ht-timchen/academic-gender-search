#!/usr/bin/env python3
"""
Script to add total_projects data from chief_investigators_data.json 
to ci_gender.json based on name matching.
"""

import json
import os

def normalize_name(name):
    """
    Normalize names for better matching by removing common prefixes and 
    standardizing format
    """
    # Remove common academic prefixes
    prefixes = ['Prof ', 'Dr ', 'A/Prof ', 'Assoc Prof ', 'Associate Prof ', 'Hon Prof ', 'Hon A/Prof ']
    normalized = name
    for prefix in prefixes:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):]
            break
    
    # Strip whitespace and convert to lowercase for comparison
    return normalized.strip().lower()

def add_project_counts(chief_investigators_file, ci_gender_file, output_file):
    """
    Add total_projects from chief_investigators_data.json to ci_gender.json
    """
    
    print("Loading chief investigators data...")
    with open(chief_investigators_file, 'r') as f:
        chief_data = json.load(f)
    
    print("Loading gender analysis data...")
    with open(ci_gender_file, 'r') as f:
        gender_data = json.load(f)
    
    # Create lookup dictionary from chief investigators data
    print("Creating name lookup dictionary...")
    name_to_projects = {}
    
    for ci in chief_data['unique_chief_investigators']:
        normalized_name = normalize_name(ci['name'])
        name_to_projects[normalized_name] = {
            'original_name': ci['name'],
            'total_projects': ci['total_projects'],
            'affiliations': ci['affiliations']
        }
    
    print(f"Found {len(name_to_projects)} researchers in chief investigators data")
    
    # Add project counts to gender data
    matches_found = 0
    no_matches = []
    
    print("Matching names and adding project counts...")
    
    for researcher in gender_data['results']:
        normalized_name = normalize_name(researcher['name'])
        
        if normalized_name in name_to_projects:
            # Found a match
            researcher['total_projects'] = name_to_projects[normalized_name]['total_projects']
            matches_found += 1
        else:
            # No match found
            researcher['total_projects'] = None
            no_matches.append(researcher['name'])
    
    # Save the updated data
    print(f"Saving updated data to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(gender_data, f, indent=2)
    
    # Print statistics
    print("\n" + "="*60)
    print("PROJECT COUNT MERGE COMPLETE")
    print("="*60)
    print(f"Total researchers in gender data: {len(gender_data['results'])}")
    print(f"Matches found: {matches_found}")
    print(f"No matches: {len(no_matches)}")
    print(f"Match rate: {matches_found/len(gender_data['results'])*100:.1f}%")
    
    if no_matches:
        print(f"\nFirst 10 researchers without project count matches:")
        for name in no_matches[:10]:
            print(f"  - {name}")
        
        if len(no_matches) > 10:
            print(f"  ... and {len(no_matches) - 10} more")
    
    print(f"\nUpdated data saved to: {output_file}")
    
    return matches_found, len(no_matches)

def main():
    """Main function"""
    
    # File paths
    chief_investigators_file = "chief_investigators_data.json"
    ci_gender_file = "ci_gender.json"
    output_file = "ci_gender_with_projects.json"
    
    # Check if input files exist
    if not os.path.exists(chief_investigators_file):
        print(f"❌ Error: {chief_investigators_file} not found!")
        return
    
    if not os.path.exists(ci_gender_file):
        print(f"❌ Error: {ci_gender_file} not found!")
        return
    
    print("🔄 Adding project counts to gender analysis data...")
    print(f"📊 Source: {chief_investigators_file}")
    print(f"🎯 Target: {ci_gender_file}")
    print(f"💾 Output: {output_file}")
    print()
    
    try:
        matches, no_matches = add_project_counts(
            chief_investigators_file, 
            ci_gender_file, 
            output_file
        )
        
        print("\n✅ Successfully added project counts!")
        
        if matches > 0:
            print(f"🎉 {matches} researchers now have project count information")
        
        if no_matches > 0:
            print(f"⚠️  {no_matches} researchers still need manual matching")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return

if __name__ == "__main__":
    main()
