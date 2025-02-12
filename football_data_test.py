import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FootballData:
    def __init__(self):
        self.api_key = os.getenv('FOOTBALL_DATA_API_KEY')
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {
            'X-Auth-Token': self.api_key
        }

    def get_champions_league_matches(self):
        """Get Champions League matches for today"""
        # Champions League competition ID is 2001
        url = f"{self.base_url}/competitions/CL/matches"
        
        # Get today's date
        today = datetime.now().strftime('%Y-%m-%d')
        
        params = {
            'dateFrom': today,
            'dateTo': today,
            'status': 'SCHEDULED,LIVE,IN_PLAY,PAUSED'
        }
        
        print(f"\nChecking Champions League matches for {today}")
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            print(f"API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get('matches', [])
                
                if matches:
                    print(f"\nFound {len(matches)} Champions League matches:")
                    for match in matches:
                        match_date = datetime.strptime(match.get('utcDate', ''), '%Y-%m-%dT%H:%M:%SZ')
                        local_time = match_date.strftime('%H:%M')
                        
                        home_team = match.get('homeTeam', {}).get('name')
                        away_team = match.get('awayTeam', {}).get('name')
                        status = match.get('status')
                        stage = match.get('stage')
                        
                        print(f"\n{local_time}: {home_team} vs {away_team}")
                        print(f"Stage: {stage}")
                        print(f"Status: {status}")
                else:
                    print("\nNo Champions League matches found for today")
                    
                # Print rate limit info
                if 'X-Requests-Available-Minute' in response.headers:
                    print(f"\nAPI Rate Limit: {response.headers['X-Requests-Available-Minute']} requests remaining this minute")
            
            elif response.status_code == 403:
                print("Error: API key required. Please set FOOTBALL_DATA_API_KEY in your .env file")
            else:
                print(f"Error: API returned status code {response.status_code}")
                print(response.text)
                
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")

def main():
    api = FootballData()
    api.get_champions_league_matches()

if __name__ == "__main__":
    main()
