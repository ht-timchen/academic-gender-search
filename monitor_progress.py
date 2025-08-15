#!/usr/bin/env python3
import json
import time
import os
from datetime import datetime

def monitor_progress():
    """Monitor the progress of CI processing"""
    
    results_file = 'ci_short_search_results.json'
    total_cis = 2679
    
    print("CI Gender Analyzer Progress Monitor")
    print("=" * 50)
    print(f"Target: {total_cis} CIs")
    print("Press Ctrl+C to stop monitoring\n")
    
    try:
        while True:
            if os.path.exists(results_file):
                try:
                    with open(results_file, 'r') as f:
                        data = json.load(f)
                    
                    processed = len(data.get('results', []))
                    percentage = (processed / total_cis) * 100
                    
                    print(f"\r[{datetime.now().strftime('%H:%M:%S')}] Progress: {processed}/{total_cis} ({percentage:.1f}%) ", end="", flush=True)
                    
                    if processed > 0:
                        latest = data['results'][-1]
                        successful_searches = sum(1 for r in data['results'] if r.get('search_successful', False))
                        success_rate = (successful_searches / processed) * 100
                        
                        if processed % 10 == 0:  # Detailed update every 10 CIs
                            print(f"\n  Latest: {latest['name']}")
                            print(f"  Success rate: {successful_searches}/{processed} ({success_rate:.1f}%)")
                            print(f"  Estimated time remaining: {((total_cis - processed) * 2) / 60:.1f} minutes")
                    
                    if processed >= total_cis:
                        print(f"\n🎉 Processing complete! {processed} CIs analyzed.")
                        break
                        
                except json.JSONDecodeError:
                    print(f"\r[{datetime.now().strftime('%H:%M:%S')}] Waiting for valid JSON...", end="", flush=True)
                except Exception as e:
                    print(f"\r[{datetime.now().strftime('%H:%M:%S')}] Error: {e}", end="", flush=True)
            else:
                print(f"\r[{datetime.now().strftime('%H:%M:%S')}] Waiting for results file...", end="", flush=True)
            
            time.sleep(5)  # Check every 5 seconds
            
    except KeyboardInterrupt:
        print(f"\n\nMonitoring stopped.")
        if os.path.exists(results_file):
            try:
                with open(results_file, 'r') as f:
                    data = json.load(f)
                processed = len(data.get('results', []))
                print(f"Final count: {processed}/{total_cis} CIs processed")
            except:
                print("Could not read final count")

if __name__ == "__main__":
    monitor_progress()


