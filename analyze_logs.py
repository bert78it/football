import re
from datetime import datetime
import sys
from collections import defaultdict
import json

def analyze_log_file(file_path):
    """Analyze the log file and extract useful information"""
    match_counts = defaultdict(int)
    notification_counts = defaultdict(int)
    errors = []
    api_calls = []
    
    # Patterns to match
    match_pattern = re.compile(r"Found (\d+) matches from Football-Data\.org")
    notification_pattern = re.compile(r"Sent Telegram notification for match: (.*?) vs (.*?)$")
    error_pattern = re.compile(r"ERROR.*?: (.*?)$")
    api_pattern = re.compile(r"API Response Headers.*?X-Requests-Available-Minute: (\d+)")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        print(f"\n📊 Log Analysis Report")
        print(f"{'='*50}")
        
        # Analyze each line
        current_date = None
        for line in lines:
            # Extract timestamp
            timestamp_match = re.match(r"(\d{4}-\d{2}-\d{2})", line)
            if timestamp_match:
                current_date = timestamp_match.group(1)
            
            # Count matches found
            if match := match_pattern.search(line):
                count = int(match.group(1))
                match_counts[current_date] = count
            
            # Count notifications sent
            if match := notification_pattern.search(line):
                home, away = match.groups()
                notification_counts[f"{home} vs {away}"] += 1
            
            # Collect errors
            if match := error_pattern.search(line):
                errors.append(match.group(1))
            
            # Track API usage
            if match := api_pattern.search(line):
                api_calls.append(int(match.group(1)))
        
        # Report: Matches Found
        print("\n📅 Matches Found by Date:")
        print("-" * 30)
        for date, count in match_counts.items():
            print(f"{date}: {count} matches")
        
        # Report: Notifications
        print("\n📬 Notifications Sent:")
        print("-" * 30)
        for match, count in notification_counts.items():
            print(f"{match}: {count} notifications")
        
        # Report: API Usage
        if api_calls:
            print("\n🔄 API Usage:")
            print("-" * 30)
            print(f"Average requests remaining: {sum(api_calls)/len(api_calls):.1f}")
            print(f"Lowest requests remaining: {min(api_calls)}")
        
        # Report: Errors
        if errors:
            print("\n⚠️ Errors Found:")
            print("-" * 30)
            for error in errors:
                print(f"- {error}")
        
        # Save report to file
        report = {
            'matches_by_date': dict(match_counts),
            'notifications': dict(notification_counts),
            'api_calls': api_calls,
            'errors': errors
        }
        
        with open('log_analysis_report.json', 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        print("\n📋 Report saved to log_analysis_report.json")
        
    except FileNotFoundError:
        print(f"Error: Could not find log file at {file_path}")
    except Exception as e:
        print(f"Error analyzing logs: {str(e)}")

if __name__ == "__main__":
    log_file = 'football_notifications.log'
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    analyze_log_file(log_file)
