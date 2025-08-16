#!/usr/bin/env python3
"""
Script to visualize gender ratios by project count using bar charts.
Creates visualizations showing how gender distribution varies with number of projects.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import seaborn as sns

def load_data(filename):
    """Load the gender data with project counts"""
    with open(filename, 'r') as f:
        data = json.load(f)
    return data['results']

def analyze_gender_by_projects(researchers):
    """Analyze gender distribution by project count"""
    
    # Group by project count
    project_gender_data = defaultdict(lambda: {'male': 0, 'female': 0, 'unknown': 0})
    
    for researcher in researchers:
        project_count = researcher.get('total_projects', 0)
        gender = researcher.get('gender', 'unknown')
        project_gender_data[project_count][gender] += 1
    
    return dict(project_gender_data)

def create_gender_ratio_chart(project_data, output_file='gender_by_projects.png'):
    """Create bar chart showing gender ratios by project count"""
    
    # Prepare data for plotting
    project_counts = sorted(project_data.keys())
    male_counts = [project_data[pc]['male'] for pc in project_counts]
    female_counts = [project_data[pc]['female'] for pc in project_counts]
    unknown_counts = [project_data[pc]['unknown'] for pc in project_counts]
    
    # Calculate totals for each project count
    totals = [male_counts[i] + female_counts[i] + unknown_counts[i] for i in range(len(project_counts))]
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Chart 1: Absolute counts
    x = np.arange(len(project_counts))
    width = 0.8
    
    p1 = ax1.bar(x, male_counts, width, label='Male', color='#4472C4', alpha=0.8)
    p2 = ax1.bar(x, female_counts, width, bottom=male_counts, label='Female', color='#E15759', alpha=0.8)
    p3 = ax1.bar(x, unknown_counts, width, 
                bottom=[male_counts[i] + female_counts[i] for i in range(len(project_counts))], 
                label='Unknown', color='#70AD47', alpha=0.8)
    
    ax1.set_xlabel('Number of Projects')
    ax1.set_ylabel('Number of Researchers')
    ax1.set_title('Gender Distribution by Project Count\n(Absolute Numbers)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(project_counts)
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for i, (male, female, unknown, total) in enumerate(zip(male_counts, female_counts, unknown_counts, totals)):
        if total > 0:  # Only add label if there are researchers
            ax1.text(i, total + max(totals) * 0.01, str(total), 
                    ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    # Chart 2: Percentage ratios
    male_pct = [male_counts[i] / totals[i] * 100 if totals[i] > 0 else 0 for i in range(len(project_counts))]
    female_pct = [female_counts[i] / totals[i] * 100 if totals[i] > 0 else 0 for i in range(len(project_counts))]
    unknown_pct = [unknown_counts[i] / totals[i] * 100 if totals[i] > 0 else 0 for i in range(len(project_counts))]
    
    p1 = ax2.bar(x, male_pct, width, label='Male', color='#4472C4', alpha=0.8)
    p2 = ax2.bar(x, female_pct, width, bottom=male_pct, label='Female', color='#E15759', alpha=0.8)
    p3 = ax2.bar(x, unknown_pct, width, 
                bottom=[male_pct[i] + female_pct[i] for i in range(len(project_counts))], 
                label='Unknown', color='#70AD47', alpha=0.8)
    
    ax2.set_xlabel('Number of Projects')
    ax2.set_ylabel('Percentage of Researchers')
    ax2.set_title('Gender Distribution by Project Count\n(Percentages)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(project_counts)
    ax2.legend()
    ax2.grid(axis='y', alpha=0.3)
    ax2.set_ylim(0, 100)
    
    # Add percentage labels
    for i, (male_p, female_p, total) in enumerate(zip(male_pct, female_pct, totals)):
        if total > 0:
            ax2.text(i, male_p/2, f'{male_p:.0f}%', ha='center', va='center', 
                    fontweight='bold', color='white', fontsize=8)
            ax2.text(i, male_p + female_p/2, f'{female_p:.0f}%', ha='center', va='center', 
                    fontweight='bold', color='white', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Chart saved as: {output_file}")
    return fig

def create_detailed_analysis_chart(project_data, output_file='gender_analysis_detailed.png'):
    """Create more detailed analysis charts"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    project_counts = sorted(project_data.keys())
    male_counts = [project_data[pc]['male'] for pc in project_counts]
    female_counts = [project_data[pc]['female'] for pc in project_counts]
    unknown_counts = [project_data[pc]['unknown'] for pc in project_counts]
    totals = [male_counts[i] + female_counts[i] + unknown_counts[i] for i in range(len(project_counts))]
    
    # Chart 1: Male percentage by project count
    male_pct = [male_counts[i] / totals[i] * 100 if totals[i] > 0 else 0 for i in range(len(project_counts))]
    bars1 = ax1.bar(project_counts, male_pct, color='#4472C4', alpha=0.7)
    ax1.set_xlabel('Number of Projects')
    ax1.set_ylabel('Male Percentage (%)')
    ax1.set_title('Male Representation by Project Count')
    ax1.grid(axis='y', alpha=0.3)
    ax1.set_ylim(0, 100)
    
    # Add value labels
    for bar, pct, total in zip(bars1, male_pct, totals):
        if total > 0:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{pct:.1f}%\n(n={total})', ha='center', va='bottom', fontsize=8)
    
    # Chart 2: Female percentage by project count
    female_pct = [female_counts[i] / totals[i] * 100 if totals[i] > 0 else 0 for i in range(len(project_counts))]
    bars2 = ax2.bar(project_counts, female_pct, color='#E15759', alpha=0.7)
    ax2.set_xlabel('Number of Projects')
    ax2.set_ylabel('Female Percentage (%)')
    ax2.set_title('Female Representation by Project Count')
    ax2.grid(axis='y', alpha=0.3)
    ax2.set_ylim(0, 100)
    
    # Add value labels
    for bar, pct, total in zip(bars2, female_pct, totals):
        if total > 0:
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{pct:.1f}%\n(n={total})', ha='center', va='bottom', fontsize=8)
    
    # Chart 3: Total researchers by project count
    bars3 = ax3.bar(project_counts, totals, color='#70AD47', alpha=0.7)
    ax3.set_xlabel('Number of Projects')
    ax3.set_ylabel('Number of Researchers')
    ax3.set_title('Total Researchers by Project Count')
    ax3.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar, total in zip(bars3, totals):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(totals)*0.01, 
                str(total), ha='center', va='bottom', fontweight='bold')
    
    # Chart 4: Gender ratio (Female/Male) by project count
    gender_ratios = [female_counts[i] / male_counts[i] if male_counts[i] > 0 else 0 for i in range(len(project_counts))]
    bars4 = ax4.bar(project_counts, gender_ratios, color='#9467BD', alpha=0.7)
    ax4.set_xlabel('Number of Projects')
    ax4.set_ylabel('Female/Male Ratio')
    ax4.set_title('Gender Ratio (Female/Male) by Project Count')
    ax4.grid(axis='y', alpha=0.3)
    ax4.axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='Equal ratio (1.0)')
    ax4.legend()
    
    # Add value labels
    for bar, ratio in zip(bars4, gender_ratios):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(gender_ratios)*0.02, 
                f'{ratio:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=8)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Detailed analysis saved as: {output_file}")
    return fig

def print_summary_statistics(project_data):
    """Print summary statistics"""
    
    print("\n" + "="*80)
    print("GENDER DISTRIBUTION BY PROJECT COUNT - SUMMARY")
    print("="*80)
    
    project_counts = sorted(project_data.keys())
    
    print(f"{'Projects':<10} {'Total':<8} {'Male':<6} {'Female':<8} {'Unknown':<8} {'Male%':<7} {'Female%':<9} {'F/M Ratio':<8}")
    print("-" * 80)
    
    total_researchers = 0
    total_male = 0
    total_female = 0
    total_unknown = 0
    
    for pc in project_counts:
        male = project_data[pc]['male']
        female = project_data[pc]['female']
        unknown = project_data[pc]['unknown']
        total = male + female + unknown
        
        male_pct = (male / total * 100) if total > 0 else 0
        female_pct = (female / total * 100) if total > 0 else 0
        ratio = (female / male) if male > 0 else 0
        
        print(f"{pc:<10} {total:<8} {male:<6} {female:<8} {unknown:<8} {male_pct:<6.1f}% {female_pct:<8.1f}% {ratio:<8.2f}")
        
        total_researchers += total
        total_male += male
        total_female += female
        total_unknown += unknown
    
    print("-" * 80)
    overall_male_pct = (total_male / total_researchers * 100) if total_researchers > 0 else 0
    overall_female_pct = (total_female / total_researchers * 100) if total_researchers > 0 else 0
    overall_ratio = (total_female / total_male) if total_male > 0 else 0
    
    print(f"{'TOTAL':<10} {total_researchers:<8} {total_male:<6} {total_female:<8} {total_unknown:<8} {overall_male_pct:<6.1f}% {overall_female_pct:<8.1f}% {overall_ratio:<8.2f}")
    print("="*80)

def main():
    """Main function"""
    
    # Load data
    print("📊 Loading data from ci_gender_with_projects.json...")
    try:
        researchers = load_data('ci_gender_with_projects.json')
        print(f"✅ Loaded {len(researchers)} researchers")
    except FileNotFoundError:
        print("❌ Error: ci_gender_with_projects.json not found!")
        print("Please run add_project_counts.py first to create this file.")
        return
    
    # Analyze data
    print("🔍 Analyzing gender distribution by project count...")
    project_data = analyze_gender_by_projects(researchers)
    
    # Print summary
    print_summary_statistics(project_data)
    
    # Create visualizations
    print("\n📈 Creating visualizations...")
    
    try:
        # Basic chart
        fig1 = create_gender_ratio_chart(project_data)
        plt.show()
        
        # Detailed analysis
        fig2 = create_detailed_analysis_chart(project_data)
        plt.show()
        
        print("\n✅ Visualization complete!")
        print("📁 Charts saved as:")
        print("   - gender_by_projects.png")
        print("   - gender_analysis_detailed.png")
        
    except Exception as e:
        print(f"❌ Error creating visualizations: {e}")
        print("Make sure matplotlib and seaborn are installed:")
        print("pip install matplotlib seaborn")

if __name__ == "__main__":
    main()
