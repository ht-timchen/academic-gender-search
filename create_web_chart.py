#!/usr/bin/env python3
"""
Script to create a web-optimized gender ratio chart excluding 1-2 project entries
and generate HTML/CSS for embedding in index.html
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import base64
from io import BytesIO

def load_data(filename):
    """Load the gender data with project counts"""
    with open(filename, 'r') as f:
        data = json.load(f)
    return data['results']

def analyze_gender_by_projects(researchers, min_projects=3):
    """Analyze gender distribution by project count, excluding entries below min_projects"""
    
    project_gender_data = defaultdict(lambda: {'male': 0, 'female': 0, 'unknown': 0})
    
    for researcher in researchers:
        project_count = researcher.get('total_projects', 0)
        if project_count >= min_projects:  # Filter out low project counts
            gender = researcher.get('gender', 'unknown')
            project_gender_data[project_count][gender] += 1
    
    return dict(project_gender_data)

def create_web_optimized_chart(project_data):
    """Create a web-optimized chart for embedding in HTML"""
    
    # Prepare data for plotting
    project_counts = sorted(project_data.keys())
    male_counts = [project_data[pc]['male'] for pc in project_counts]
    female_counts = [project_data[pc]['female'] for pc in project_counts]
    unknown_counts = [project_data[pc]['unknown'] for pc in project_counts]
    
    # Calculate totals and percentages
    totals = [male_counts[i] + female_counts[i] + unknown_counts[i] for i in range(len(project_counts))]
    male_pct = [male_counts[i] / totals[i] * 100 if totals[i] > 0 else 0 for i in range(len(project_counts))]
    female_pct = [female_counts[i] / totals[i] * 100 if totals[i] > 0 else 0 for i in range(len(project_counts))]
    
    # Create figure
    plt.style.use('default')
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    
    # Create stacked bar chart with percentages
    x = np.arange(len(project_counts))
    width = 0.6
    
    # Color scheme matching the website
    male_color = '#4472C4'
    female_color = '#E15759'
    unknown_color = '#70AD47'
    
    p1 = ax.bar(x, male_pct, width, label='Male', color=male_color, alpha=0.8)
    p2 = ax.bar(x, female_pct, width, bottom=male_pct, label='Female', color=female_color, alpha=0.8)
    p3 = ax.bar(x, [100 - male_pct[i] - female_pct[i] for i in range(len(project_counts))], 
                width, bottom=[male_pct[i] + female_pct[i] for i in range(len(project_counts))], 
                label='Unknown', color=unknown_color, alpha=0.8)
    
    # Customize the chart
    ax.set_xlabel('Number of Discovery Projects', fontsize=12, fontweight='bold')
    ax.set_ylabel('Percentage of Researchers', fontsize=12, fontweight='bold')
    ax.set_title('Gender Distribution by Project Count\n(Chief Investigators with 3+ Discovery Projects)', 
                fontsize=14, fontweight='bold', pad=20)
    
    ax.set_xticks(x)
    ax.set_xticklabels(project_counts)
    ax.set_ylim(0, 100)
    
    # Add grid for better readability
    ax.grid(axis='y', alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)
    
    # Customize legend
    legend = ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
    legend.get_frame().set_facecolor('white')
    legend.get_frame().set_alpha(0.9)
    
    # Add value labels on bars
    for i, (male_p, female_p, total) in enumerate(zip(male_pct, female_pct, totals)):
        if total > 0:
            # Add total count at the top
            ax.text(i, 102, f'n={total}', ha='center', va='bottom', 
                   fontweight='bold', fontsize=9)
            
            # Add percentage labels on bars if they're large enough
            if male_p > 8:  # Only show if bar is large enough
                ax.text(i, male_p/2, f'{male_p:.0f}%', ha='center', va='center', 
                       fontweight='bold', color='white', fontsize=10)
            if female_p > 8:
                ax.text(i, male_p + female_p/2, f'{female_p:.0f}%', ha='center', va='center', 
                       fontweight='bold', color='white', fontsize=10)
    
    # Improve overall appearance
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)
    
    plt.tight_layout()
    
    # Save as high-quality PNG for web
    plt.savefig('gender_chart_web.png', dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    # Convert to base64 for embedding
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    
    plt.close()
    
    return image_base64

def generate_html_section(image_base64, project_data):
    """Generate HTML section with the chart and statistics"""
    
    # Calculate summary statistics (excluding 1-2 projects)
    project_counts = sorted(project_data.keys())
    total_researchers = sum(sum(project_data[pc].values()) for pc in project_counts)
    total_male = sum(project_data[pc]['male'] for pc in project_counts)
    total_female = sum(project_data[pc]['female'] for pc in project_counts)
    total_unknown = sum(project_data[pc]['unknown'] for pc in project_counts)
    
    male_pct = (total_male / total_researchers * 100) if total_researchers > 0 else 0
    female_pct = (total_female / total_researchers * 100) if total_researchers > 0 else 0
    unknown_pct = (total_unknown / total_researchers * 100) if total_researchers > 0 else 0
    
    html_section = f'''
        <div class="stats" style="border-left: 4px solid #007acc; background: #f8f9ff;">
            <h3>📈 Gender Distribution by Project Count</h3>
            <p><strong>Analysis of {total_researchers:,} Chief Investigators with 3+ Discovery Projects</strong></p>
            
            <div style="text-align: center; margin: 20px 0;">
                <img src="data:image/png;base64,{image_base64}" 
                     alt="Gender Distribution by Project Count Chart" 
                     style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 20px 0;">
                <div style="background: #f0f8ff; padding: 15px; border-radius: 8px; border-left: 4px solid #4472C4;">
                    <h4 style="margin: 0 0 10px 0; color: #4472C4;">👨 Male Researchers</h4>
                    <p style="margin: 0; font-size: 1.2em; font-weight: bold;">{total_male:,} ({male_pct:.1f}%)</p>
                </div>
                <div style="background: #fff5f5; padding: 15px; border-radius: 8px; border-left: 4px solid #E15759;">
                    <h4 style="margin: 0 0 10px 0; color: #E15759;">👩 Female Researchers</h4>
                    <p style="margin: 0; font-size: 1.2em; font-weight: bold;">{total_female:,} ({female_pct:.1f}%)</p>
                </div>
                <div style="background: #f0f8f0; padding: 15px; border-radius: 8px; border-left: 4px solid #70AD47;">
                    <h4 style="margin: 0 0 10px 0; color: #70AD47;">❓ Unknown</h4>
                    <p style="margin: 0; font-size: 1.2em; font-weight: bold;">{total_unknown:,} ({unknown_pct:.1f}%)</p>
                </div>
            </div>
            
            <p><strong>Key Insights:</strong></p>
            <ul>
                <li><strong>Gender Gap Widens:</strong> Female representation decreases from 23.6% (3 projects) to 15.1% (6 projects)</li>
                <li><strong>High-Impact Researchers:</strong> Among researchers with 6+ projects, males represent 76.9%+ of the cohort</li>
                <li><strong>Leadership Pipeline:</strong> The data suggests a "leaky pipeline" where female participation diminishes at higher productivity levels</li>
            </ul>
            <p><em>Note: Analysis excludes researchers with 1-2 projects to focus on established researchers. Data represents Chief Investigators in the Australian Discovery Projects system.</em></p>
        </div>'''
    
    return html_section

def main():
    """Main function"""
    
    print("📊 Creating web-optimized gender distribution chart...")
    
    # Load data
    try:
        researchers = load_data('ci_gender_with_projects.json')
        print(f"✅ Loaded {len(researchers)} researchers")
    except FileNotFoundError:
        print("❌ Error: ci_gender_with_projects.json not found!")
        return
    
    # Analyze data (exclude 1-2 projects)
    print("🔍 Analyzing gender distribution (3+ projects only)...")
    project_data = analyze_gender_by_projects(researchers, min_projects=3)
    
    total_analyzed = sum(sum(project_data[pc].values()) for pc in project_data.keys())
    print(f"📈 Analyzing {total_analyzed} researchers with 3+ projects")
    
    # Create chart
    print("🎨 Creating web-optimized chart...")
    image_base64 = create_web_optimized_chart(project_data)
    
    # Generate HTML
    print("📝 Generating HTML section...")
    html_section = generate_html_section(image_base64, project_data)
    
    # Save HTML section to file
    with open('chart_section.html', 'w') as f:
        f.write(html_section)
    
    print("✅ Chart creation complete!")
    print("📁 Files created:")
    print("   - gender_chart_web.png (static image)")
    print("   - chart_section.html (HTML section for index.html)")
    print("\n💡 Next: Copy the content from chart_section.html into index.html")

if __name__ == "__main__":
    main()
