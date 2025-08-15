#!/usr/bin/env python3
"""
Convert CI analysis results to CSV format for further analysis.
"""

import json
import csv
from pathlib import Path

def convert_to_csv():
    # Read the JSON results
    with open('ci_short_search_results.json', 'r') as f:
        data = json.load(f)
    
    results = data['results']
    
    # Create CSV output
    output_file = 'data/output/australian_academics_gender_analysis.csv'
    Path('data/output').mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'name',
            'primary_affiliation', 
            'all_affiliations',
            'gender',
            'confidence',
            'summary',
            'research_areas',
            'web_sources_found',
            'search_successful',
            'search_notes'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for entry in results:
            # Process affiliations
            affiliations = entry.get('affiliations', [])
            primary_affiliation = affiliations[0] if affiliations else ''
            all_affiliations = '; '.join(affiliations)
            
            # Process research areas
            research_areas = '; '.join(entry.get('research_areas', []))
            
            # Clean summary (remove potential CSV issues)
            summary = entry.get('summary', '').replace('\n', ' ').replace('\r', ' ')
            
            writer.writerow({
                'name': entry.get('name', ''),
                'primary_affiliation': primary_affiliation,
                'all_affiliations': all_affiliations,
                'gender': entry.get('gender', 'unknown'),
                'confidence': entry.get('confidence', 'unknown'),
                'summary': summary,
                'research_areas': research_areas,
                'web_sources_found': entry.get('web_sources_found', 0),
                'search_successful': entry.get('search_successful', False),
                'search_notes': entry.get('search_notes', '')
            })
    
    print(f"Converted {len(results)} entries to {output_file}")
    
    # Create a summary statistics file
    summary_file = 'data/output/gender_analysis_statistics.csv'
    
    # Calculate statistics
    gender_counts = {}
    confidence_counts = {}
    affiliation_gender = {}
    
    for entry in results:
        gender = entry.get('gender', 'unknown')
        confidence = entry.get('confidence', 'unknown')
        
        gender_counts[gender] = gender_counts.get(gender, 0) + 1
        confidence_counts[confidence] = confidence_counts.get(confidence, 0) + 1
        
        # Track by primary affiliation
        primary_aff = entry.get('affiliations', ['Unknown'])[0]
        if primary_aff not in affiliation_gender:
            affiliation_gender[primary_aff] = {'male': 0, 'female': 0, 'unknown': 0, 'total': 0}
        affiliation_gender[primary_aff][gender] += 1
        affiliation_gender[primary_aff]['total'] += 1
    
    # Write summary statistics
    with open(summary_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Overall statistics
        writer.writerow(['OVERALL STATISTICS'])
        writer.writerow(['Category', 'Count', 'Percentage'])
        total = len(results)
        
        for gender, count in sorted(gender_counts.items()):
            percentage = (count / total) * 100
            writer.writerow([f'Gender: {gender}', count, f'{percentage:.1f}%'])
        
        writer.writerow([])
        
        for conf, count in sorted(confidence_counts.items()):
            percentage = (count / total) * 100
            writer.writerow([f'Confidence: {conf}', count, f'{percentage:.1f}%'])
        
        writer.writerow([])
        writer.writerow(['BY INSTITUTION'])
        writer.writerow(['Institution', 'Total', 'Male', 'Female', 'Unknown', 'Female %'])
        
        # Sort institutions by total count
        sorted_institutions = sorted(affiliation_gender.items(), 
                                   key=lambda x: x[1]['total'], reverse=True)
        
        for institution, counts in sorted_institutions:
            if counts['total'] >= 5:  # Only show institutions with 5+ academics
                female_pct = (counts['female'] / counts['total']) * 100 if counts['total'] > 0 else 0
                writer.writerow([
                    institution,
                    counts['total'],
                    counts['male'],
                    counts['female'], 
                    counts['unknown'],
                    f'{female_pct:.1f}%'
                ])
    
    print(f"Summary statistics saved to {summary_file}")

if __name__ == "__main__":
    convert_to_csv()
