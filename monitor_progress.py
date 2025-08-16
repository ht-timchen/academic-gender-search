#!/usr/bin/env python3
"""
Monitor the progress of the gender analyzer script
"""
import json
import time
import os
from datetime import datetime

def get_progress_stats():
    """Get current progress statistics"""
    try:
        # Load cache file to check progress
        with open('ci_short_search_cache.json', 'r') as f:
            cache_data = json.load(f)
        
        results = cache_data.get('results', [])
        total_analyzed = len(results)
        
        # Get gender distribution
        gender_counts = {}
        successful_searches = 0
        total_sources = 0
        
        for result in results:
            gender = result.get('gender', 'unknown')
            gender_counts[gender] = gender_counts.get(gender, 0) + 1
            if result.get('search_successful'):
                successful_searches += 1
            total_sources += result.get('web_sources_found', 0)
        
        return {
            'total_analyzed': total_analyzed,
            'gender_counts': gender_counts,
            'successful_searches': successful_searches,
            'total_sources': total_sources,
            'last_processed': results[-1]['name'] if results else 'None'
        }
    except Exception as e:
        return {'error': str(e)}

def monitor_progress(interval=30):
    """Monitor progress and display updates"""
    print("🔍 Gender Analyzer Progress Monitor")
    print("=" * 50)
    
    while True:
        stats = get_progress_stats()
        
        if 'error' in stats:
            print(f"❌ Error reading progress: {stats['error']}")
            time.sleep(interval)
            continue
        
        # Clear screen and show current status
        os.system('clear' if os.name == 'posix' else 'cls')
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"🔍 Gender Analyzer Progress Monitor - {current_time}")
        print("=" * 60)
        
        print(f"📊 Total Analyzed: {stats['total_analyzed']} researchers")
        print(f"👤 Last Processed: {stats['last_processed']}")
        print()
        
        print("📈 Gender Distribution:")
        for gender, count in stats['gender_counts'].items():
            percentage = (count / stats['total_analyzed']) * 100 if stats['total_analyzed'] > 0 else 0
            print(f"  {gender.capitalize()}: {count} ({percentage:.1f}%)")
        print()
        
        success_rate = (stats['successful_searches'] / stats['total_analyzed'] * 100) if stats['total_analyzed'] > 0 else 0
        avg_sources = (stats['total_sources'] / stats['total_analyzed']) if stats['total_analyzed'] > 0 else 0
        
        print("🔍 Search Statistics:")
        print(f"  Successful searches: {stats['successful_searches']}/{stats['total_analyzed']} ({success_rate:.1f}%)")
        print(f"  Total sources found: {stats['total_sources']}")
        print(f"  Average sources per researcher: {avg_sources:.1f}")
        print()
        
        print(f"⏱️  Next update in {interval} seconds... (Ctrl+C to stop)")
        
        try:
            time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n👋 Monitoring stopped.")
            break

if __name__ == "__main__":
    monitor_progress()