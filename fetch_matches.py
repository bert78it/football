import os
import json
import logging
import requests
from datetime import datetime, timezone, timedelta
from icalendar import Calendar, Event
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
logging.info("Loading environment variables...")
load_dotenv(verbose=True)

# Debug environment variables
api_football_key = os.getenv('API_FOOTBALL_KEY')
football_data_key = os.getenv('FOOTBALL_DATA_API_KEY')
logging.info(f"API_FOOTBALL_KEY present: {bool(api_football_key)}")
logging.info(f"FOOTBALL_DATA_API_KEY present: {bool(football_data_key)}")

def get_matches_from_api_football():
    """Fetch matches from API-Football"""
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    api_key = os.getenv('API_FOOTBALL_KEY')
    
    if not api_key:
        logging.warning("API-Football key not found in environment variables")
        return []

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    # Get today's date in YYYY-MM-DD format
    today = datetime.now().strftime("%Y-%m-%d")
    
    # List of league IDs to fetch
    leagues = [
        135,  # Serie A
        2,    # Champions League
        3,    # Europa League
        39,   # Premier League
        140,  # La Liga
        78,   # Bundesliga
        61,   # Ligue 1
        71,   # Serie B
        848,  # Conference League
        81    # Coppa Italia
    ]
    
    all_matches = []
    seen_matches = set()

    for league in leagues:
        try:
            params = {
                "date": today,
                "league": str(league),
                "timezone": "Europe/Rome"
            }

            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 401:
                logging.error("API-Football error: Invalid API key")
                return []
            response.raise_for_status()
            data = response.json()
            
            if not data.get('response'):
                logging.info(f"No matches found for league {league}")
                continue
                
            for fixture in data.get('response', []):
                match_key = (
                    fixture['teams']['home']['name'],
                    fixture['teams']['away']['name'],
                    fixture['fixture']['date']
                )
                
                if match_key not in seen_matches:
                    seen_matches.add(match_key)
                    match = {
                        'home_team': fixture['teams']['home']['name'],
                        'away_team': fixture['teams']['away']['name'],
                        'date': fixture['fixture']['date'],
                        'venue': fixture['fixture']['venue']['name'] if fixture['fixture'].get('venue') else None,
                        'status': fixture['fixture']['status']['long'],
                        'source': 'API-Football',
                        'competition': fixture['league']['name']
                    }
                    all_matches.append(match)
            
            # Add a small delay between requests to respect rate limits
            import time
            time.sleep(1)
            
        except Exception as e:
            logging.error(f"Error fetching matches for league {league}: {e}")
            continue
    
    logging.info(f"Found {len(all_matches)} matches from API-Football")
    return all_matches

def get_matches_from_football_data():
    """Fetch matches from Football-Data.org"""
    api_key = os.getenv('FOOTBALL_DATA_API_KEY')
    if not api_key:
        logging.warning("Football-Data.org API key not found in environment variables")
        return []

    headers = {'X-Auth-Token': api_key}
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    url = f"http://api.football-data.org/v4/matches?date={today}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logging.error(f"Error fetching matches from Football-Data.org: {response.status_code}")
            return []

        data = response.json()
        matches = []
        for match in data.get('matches', []):
            # Skip matches without both teams
            if not match.get('homeTeam') or not match.get('awayTeam'):
                continue
                
            match_data = {
                'home_team': match['homeTeam'].get('name', 'Unknown Team'),
                'away_team': match['awayTeam'].get('name', 'Unknown Team'),
                'date': match.get('utcDate'),
                'venue': match.get('venue'),
                'status': match.get('status'),
                'source': 'Football-Data.org',
                'competition': match.get('competition', {}).get('name', 'Unknown Competition')
            }
            matches.append(match_data)

        logging.info(f"Found {len(matches)} matches from Football-Data.org")
        return matches

    except Exception as e:
        logging.error(f"Error fetching matches from Football-Data.org: {str(e)}")
        return []

def create_calendar_file(matches):
    """Create an ICS calendar file with the matches"""
    cal = Calendar()
    cal.add('prodid', '-//Football Matches Calendar//EN')
    cal.add('version', '2.0')
    cal.add('calscale', 'GREGORIAN')
    cal.add('method', 'PUBLISH')
    cal.add('x-wr-calname', 'Football Matches')
    cal.add('x-wr-timezone', 'Europe/Rome')

    # Track unique events
    seen_events = set()

    for match in matches:
        # Create a unique key for the match
        match_key = (match['home_team'], match['away_team'], match['date'])
        
        if match_key not in seen_events:
            seen_events.add(match_key)
            event = Event()
            
            # Create consistent event UID
            match_date = datetime.strptime(match['date'], '%Y-%m-%dT%H:%M:%S%z').strftime('%Y%m%d')
            teams_key = f"{match['home_team']}_{match['away_team']}".replace(' ', '').lower()
            uid = f"football_match_{match_date}_{teams_key}@football_calendar"
            
            # Basic event information
            summary = f"{match['home_team']} vs {match['away_team']}"
            event.add('summary', summary)
            event.add('uid', uid)
            
            # Parse and set the date
            match_time = datetime.strptime(match['date'], '%Y-%m-%dT%H:%M:%S%z')
            event.add('dtstart', match_time)
            event.add('dtend', match_time + timedelta(hours=2))
            event.add('dtstamp', datetime.now(timezone.utc))
            
            # Location and description
            if match.get('venue'):
                event.add('location', match['venue'])
            
            description = (
                f"Football Match\n"
                f"Competition: {match.get('competition', 'Unknown')}\n"
                f"Status: {match['status']}\n"
                f"Source: {match['source']}"
            )
            event.add('description', description)
            
            cal.add_component(event)

    # Write to file
    with open('football_matches_calendar.ics', 'wb') as f:
        f.write(cal.to_ical())
    
    logging.info(f"Created calendar file with {len(seen_events)} unique events")

def fetch_matches():
    """Fetch matches from both APIs and save to file"""
    # Get matches from API-Football
    matches = get_matches_from_api_football()
    
    if not matches:
        logging.warning("No matches found from API-Football, trying Football-Data.org")
        matches = get_matches_from_football_data()
    
    if not matches:
        logging.warning("No matches found from any API")
        matches = []
    
    # Log the number of matches found
    logging.info(f"\nFound {len(matches)} total unique matches:")
    
    # Save matches to JSON file
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
    logging.info("Saved matches to matches.json")
    
    # Create calendar file
    create_calendar_file(matches)

if __name__ == "__main__":
    fetch_matches()
