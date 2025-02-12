import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime, timedelta
import sys

# Set console to UTF-8 mode
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Load environment variables
load_dotenv()

class APIFootball:
    def __init__(self):
        self.api_key = os.getenv('API_FOOTBALL_KEY')
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com",
            'x-rapidapi-key': self.api_key
        }

    def get_all_european_matches(self):
        """Get all European competition matches"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        # List of major European competitions
        competitions = [
            {'id': 2, 'name': 'UEFA Champions League'},
            {'id': 3, 'name': 'UEFA Europa League'},
            {'id': 848, 'name': 'UEFA Europa Conference League'},
            {'id': 4, 'name': 'UEFA Nations League'},
        ]
        
        print(f"\nChecking European matches for {today}")
        
        for comp in competitions:
            url = f"{self.base_url}/fixtures"
            params = {
                'league': comp['id'],
                'date': today,
                'timezone': 'Europe/Rome'
            }
            
            print(f"\nChecking {comp['name']} (ID: {comp['id']})...")
            
            response = requests.get(url, headers=self.headers, params=params)
            print(f"API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get('response', [])
                
                if matches:
                    print(f"Found {len(matches)} matches:")
                    for match in matches:
                        fixture = match.get('fixture', {})
                        teams = match.get('teams', {})
                        venue = fixture.get('venue', {})
                        status = fixture.get('status', {})
                        
                        match_time = datetime.strptime(fixture.get('date', ''), '%Y-%m-%dT%H:%M:%S%z')
                        local_time = match_time.strftime('%H:%M')
                        
                        print(f"\n{local_time}: {teams.get('home', {}).get('name')} vs {teams.get('away', {}).get('name')}")
                        print(f"Status: {status.get('long', 'Unknown')}")
                        print(f"Venue: {venue.get('name')} in {venue.get('city')}")
                else:
                    print("No matches found")

def main():
    api = APIFootball()
    api.get_all_european_matches()

if __name__ == "__main__":
    main()
