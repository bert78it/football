import pytz
from datetime import datetime, timedelta
import ics
import json

def load_matches(log_file='multi_source_matches.log'):
    """Load matches from log file."""
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            matches_data = json.load(f)
        return matches_data
    except Exception as e:
        print(f"Error loading matches: {e}")
        return []

def create_calendar(matches):
    """Create iCal calendar from matches."""
    calendar = ics.Calendar()
    
    for match in matches:
        try:
            # Parse match details
            home_team = match.get('home_team', 'Unknown')
            away_team = match.get('away_team', 'Unknown')
            match_time = match.get('datetime')
            competition = match.get('competition', 'Football Match')
            
            # Convert to datetime
            match_datetime = datetime.fromisoformat(match_time)
            match_datetime = match_datetime.replace(tzinfo=pytz.UTC)
            
            # Create calendar event
            event = ics.Event()
            event.name = f"{home_team} vs {away_team}"
            event.description = f"{competition}: {home_team} vs {away_team}"
            event.begin = match_datetime
            event.duration = timedelta(hours=2)  # Typical match duration
            
            calendar.events.add(event)
        except Exception as e:
            print(f"Error processing match: {e}")
    
    return calendar

def save_calendar(calendar, filename='football_matches.ics'):
    """Save calendar to .ics file."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(calendar)
    print(f"Calendar saved to {filename}")

def main():
    matches = load_matches()
    calendar = create_calendar(matches)
    save_calendar(calendar)

if __name__ == '__main__':
    main()
