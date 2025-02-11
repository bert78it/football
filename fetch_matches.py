import os
import requests
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables
load_dotenv()

class FootballAPI:
    def __init__(self):
        # API-Football configuration
        self.api_football_key = os.getenv('API_FOOTBALL_KEY')
        self.api_football_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.api_football_headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': self.api_football_key
        }
        
        # Football-Data.org configuration
        self.football_data_key = os.getenv('FOOTBALL_DATA_API_KEY')
        self.football_data_url = "https://api.football-data.org/v4"
        self.football_data_headers = {
            'X-Auth-Token': self.football_data_key
        }

    def get_matches_from_api_football(self):
        """Get matches from API-Football"""
        today = datetime.now().strftime('%Y-%m-%d')
        matches = []
        
        # Champions League ID in API-Football is 2
        url = f"{self.api_football_url}/fixtures"
        params = {
            'league': 2,
            'date': today,
            'timezone': 'Europe/Rome'
        }
        
        try:
            response = requests.get(url, headers=self.api_football_headers, params=params)
            if response.status_code == 200:
                data = response.json()
                api_matches = data.get('response', [])
                
                for match in api_matches:
                    fixture = match.get('fixture', {})
                    teams = match.get('teams', {})
                    venue = fixture.get('venue', {})
                    
                    match_info = {
                        'date': fixture.get('date'),
                        'home_team': teams.get('home', {}).get('name'),
                        'away_team': teams.get('away', {}).get('name'),
                        'venue': venue.get('name'),
                        'city': venue.get('city'),
                        'status': fixture.get('status', {}).get('long'),
                        'source': 'API-Football'
                    }
                    matches.append(match_info)
                
                logging.info(f"Found {len(matches)} matches from API-Football")
            else:
                logging.error(f"API-Football error: {response.status_code}")
                
        except Exception as e:
            logging.error(f"Error fetching from API-Football: {e}")
        
        return matches

    def get_matches_from_football_data(self):
        """Get matches from Football-Data.org"""
        today = datetime.now().strftime('%Y-%m-%d')
        matches = []
        
        url = f"{self.football_data_url}/competitions/CL/matches"
        params = {
            'dateFrom': today,
            'dateTo': today,
            'status': 'SCHEDULED,LIVE,IN_PLAY,PAUSED'
        }
        
        try:
            response = requests.get(url, headers=self.football_data_headers, params=params)
            if response.status_code == 200:
                data = response.json()
                api_matches = data.get('matches', [])
                
                for match in api_matches:
                    match_info = {
                        'date': match.get('utcDate'),
                        'home_team': match.get('homeTeam', {}).get('name'),
                        'away_team': match.get('awayTeam', {}).get('name'),
                        'venue': match.get('venue'),
                        'status': match.get('status'),
                        'stage': match.get('stage'),
                        'source': 'Football-Data.org'
                    }
                    matches.append(match_info)
                
                logging.info(f"Found {len(matches)} matches from Football-Data.org")
            else:
                logging.error(f"Football-Data.org error: {response.status_code}")
                
        except Exception as e:
            logging.error(f"Error fetching from Football-Data.org: {e}")
        
        return matches

    def get_all_matches(self):
        """Get matches from both APIs and combine results"""
        all_matches = []
        
        # Try API-Football first
        api_football_matches = self.get_matches_from_api_football()
        if api_football_matches:
            all_matches.extend(api_football_matches)
            logging.info("Successfully fetched matches from API-Football")
        else:
            logging.warning("No matches found from API-Football, trying Football-Data.org")
        
        # Try Football-Data.org as backup
        football_data_matches = self.get_matches_from_football_data()
        if football_data_matches:
            # Only add matches that aren't already in the list
            for match in football_data_matches:
                if not any(
                    m['home_team'] == match['home_team'] and 
                    m['away_team'] == match['away_team'] 
                    for m in all_matches
                ):
                    all_matches.append(match)
            logging.info("Successfully fetched matches from Football-Data.org")
        else:
            logging.warning("No matches found from Football-Data.org")
        
        return all_matches

def main():
    api = FootballAPI()
    matches = api.get_all_matches()
    
    if matches:
        logging.info(f"\nFound {len(matches)} total matches:")
        for match in matches:
            match_time = datetime.strptime(match['date'], '%Y-%m-%dT%H:%M:%S%z')
            local_time = match_time.strftime('%H:%M')
            
            logging.info(f"\n{local_time}: {match['home_team']} vs {match['away_team']}")
            logging.info(f"Status: {match['status']}")
            if match.get('venue'):
                logging.info(f"Venue: {match['venue']}")
            logging.info(f"Source: {match['source']}")
    else:
        logging.warning("No matches found from any API")

if __name__ == "__main__":
    main()
