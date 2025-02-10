import pytz
from datetime import datetime, timedelta
import ics
import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

def load_matches(log_file='multi_source_matches.log'):
    """Load matches from log file."""
    try:
        # Try JSON first
        with open(log_file, 'r', encoding='utf-8') as f:
            matches_data = json.load(f)
        return matches_data
    except json.JSONDecodeError:
        # Fallback to reading raw log
        logging.warning(f"Could not parse {log_file} as JSON. Attempting alternative parsing.")
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                log_content = f.read()
                # Add custom parsing logic here if needed
                logging.info(f"Log content: {log_content[:500]}...")
            return []
        except Exception as e:
            logging.error(f"Error reading log file: {e}")
            return []

def create_calendar(matches):
    """Create iCal calendar from matches."""
    calendar = ics.Calendar()
    
    for match in matches:
        try:
            # More robust match parsing
            home_team = match.get('home_team', match.get('homeTeam', 'Unknown Home'))
            away_team = match.get('away_team', match.get('awayTeam', 'Unknown Away'))
            match_time = match.get('datetime', match.get('date', None))
            competition = match.get('competition', match.get('league', 'Football Match'))
            
            if not match_time:
                logging.warning(f"Skipping match without datetime: {match}")
                continue
            
            # Convert to datetime
            match_datetime = datetime.fromisoformat(match_time) if isinstance(match_time, str) else match_time
            match_datetime = match_datetime.replace(tzinfo=pytz.UTC)
            
            # Create calendar event
            event = ics.Event()
            event.name = f"{home_team} vs {away_team}"
            event.description = f"{competition}: {home_team} vs {away_team}"
            event.begin = match_datetime
            event.duration = timedelta(hours=2)  # Typical match duration
            
            calendar.events.add(event)
        except Exception as e:
            logging.error(f"Error processing match: {e}")
    
    return calendar

def save_calendar(calendar, filename='football_matches.ics'):
    """Save calendar to .ics file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(calendar)
        logging.info(f"Calendar saved to {filename}")
        return True
    except Exception as e:
        logging.error(f"Error saving calendar: {e}")
        return False

def main():
    # Try multiple log file names
    log_files = ['multi_source_matches.log', 'football_matches.log']
    
    for log_file in log_files:
        if os.path.exists(log_file):
            logging.info(f"Attempting to load matches from {log_file}")
            matches = load_matches(log_file)
            
            if matches:
                calendar = create_calendar(matches)
                save_calendar(calendar)
                return
    
    logging.error("No valid log files found to generate calendar.")

if __name__ == '__main__':
    main()
