import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(funcName)s] %(message)s',
    filename='multi_source_matches.log',
    filemode='a',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class FootballDataSources:
    def __init__(self):
        # API Configuration with additional validation
        self.apis = {
            'football_data': {
                'key': os.getenv('FOOTBALL_DATA_API_KEY', ''),
                'base_url': 'https://api.football-data.org/v4',
                'rate_limit': 10  # requests per minute
            },
            'rapidapi': {
                'key': os.getenv('RAPIDAPI_KEY', ''),
                'host': 'api-football-v1.p.rapidapi.com',
                'base_url': 'https://api-football-v1.p.rapidapi.com/v3',
                'rate_limit': 30  # requests per minute
            },
            'sportmonks': {
                'key': os.getenv('SPORTMONKS_API_KEY', ''),
                'base_url': 'https://api.sportmonks.com/v3',
                'rate_limit': 20  # requests per minute
            },
            'odds_api': {
                'key': os.getenv('ODDS_API_KEY', ''),
                'base_url': 'https://api.the-odds-api.com/v4',
                'rate_limit': 50  # requests per minute
            },
            'api_sports': {
                'key': os.getenv('API_SPORTS_KEY', ''),
                'base_url': 'https://api-football-v1.p.rapidapi.com/v3',
                'rate_limit': 30  # requests per minute
            }
        }

    def _validate_api_key(self, api_name):
        """Enhanced API key validation with detailed logging"""
        api_key = self.apis.get(api_name, {}).get('key', '')
        if not api_key:
            logger.warning(f"No API key found for {api_name}. Skipping this data source.")
            return False
        return True

    def fetch_football_data_matches(self, date=None):
        """Fetch matches from football-data.org with specific requirements"""
        if not self._validate_api_key('football_data'):
            return []

        date = date or datetime.now().strftime('%Y-%m-%d')
        
        try:
            headers = {
                'X-Auth-Token': self.apis['football_data']['key'],
                'Accept': 'application/json'
            }
            
            url = f"{self.apis['football_data']['base_url']}/matches"
            
            params = {
                'dateFrom': date,
                'dateTo': date,
                'status': 'SCHEDULED'  # Only get scheduled matches
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                matches_data = response.json().get('matches', [])
                
                matches = []
                for match in matches_data:
                    match_info = {
                        'source': 'football-data.org',
                        'competition': match.get('competition', {}).get('name', 'Unknown'),
                        'home_team': match.get('homeTeam', {}).get('name', 'Unknown'),
                        'away_team': match.get('awayTeam', {}).get('name', 'Unknown'),
                        'time': match.get('utcDate', 'Unknown'),
                        'status': match.get('status', 'Unknown')
                    }
                    matches.append(match_info)
                
                return matches
            else:
                logger.error(f"Football-data.org API error: {response.status_code} - {response.text}")
                return []
        
        except requests.RequestException as e:
            logger.error(f"Football-data.org network error: {e}")
            return []

    def fetch_rapidapi_matches(self, date=None):
        """Fetch matches from RapidAPI Football with specific requirements"""
        if not self._validate_api_key('rapidapi'):
            return []

        date = date or datetime.now().strftime('%Y-%m-%d')
        
        try:
            headers = {
                'X-RapidAPI-Key': self.apis['rapidapi']['key'],
                'X-RapidAPI-Host': self.apis['rapidapi']['host']
            }
            
            url = f"{self.apis['rapidapi']['base_url']}/fixtures"
            
            params = {
                'date': date,
                'status': 'NS'  # Next Scheduled matches
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                matches_data = response.json().get('response', [])
                
                matches = []
                for match in matches_data:
                    match_info = {
                        'source': 'RapidAPI',
                        'competition': match.get('league', {}).get('name', 'Unknown'),
                        'home_team': match.get('teams', {}).get('home', {}).get('name', 'Unknown'),
                        'away_team': match.get('teams', {}).get('away', {}).get('name', 'Unknown'),
                        'time': match.get('fixture', {}).get('date', 'Unknown'),
                        'status': match.get('fixture', {}).get('status', {}).get('short', 'Unknown')
                    }
                    matches.append(match_info)
                
                return matches
            else:
                logger.error(f"RapidAPI error: {response.status_code} - {response.text}")
                return []
        
        except requests.RequestException as e:
            logger.error(f"RapidAPI network error: {e}")
            return []

    def fetch_sportmonks_matches(self, date=None):
        """Fetch matches from SportMonks with robust error handling"""
        try:
            if not self._validate_api_key('sportmonks'):
                logger.error("SportMonks API key validation failed")
                return []

            date = date or datetime.now().strftime('%Y-%m-%d')
            
            headers = {
                'Authorization': f'Bearer {self.apis["sportmonks"]["key"]}',
                'Accept': 'application/json'
            }
            
            # Detailed logging for troubleshooting
            logger.info(f"Attempting SportMonks API request for date: {date}")
            
            response = requests.get(
                f"{self.apis['sportmonks']['base_url']}/fixtures/date/{date}",
                headers=headers
            )
            
            if response.status_code == 200:
                matches_data = response.json().get('data', [])
                parsed_matches = [
                    {
                        'home_team': match.get('home_team', {}).get('name', 'Unknown'),
                        'away_team': match.get('away_team', {}).get('name', 'Unknown'),
                        'datetime': match.get('starting_at', date),
                        'competition': match.get('league', {}).get('name', 'Unknown League')
                    } for match in matches_data
                ]
                logger.info(f"Retrieved {len(parsed_matches)} matches from SportMonks")
                return parsed_matches
            else:
                logger.error(f"SportMonks API error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            logger.error(f"[fetch_sportmonks_matches] Detailed SportMonks API error: {str(e)}")
            return []

    def fetch_odds_api_matches(self, date=None):
        """Fetch matches from Odds API"""
        if not self._validate_api_key('odds_api'):
            return []

        date = date or datetime.now().strftime('%Y-%m-%d')
        
        try:
            headers = {
                'apiKey': self.apis['odds_api']['key']
            }
            
            # Odds API endpoint for upcoming matches
            url = 'https://api.the-odds-api.com/v4/sports/soccer_uefa_champs_league/odds'
            
            params = {
                'apiKey': self.apis['odds_api']['key'],
                'regions': 'eu',  # European odds
                'markets': 'h2h',  # Head-to-head market
                'oddsFormat': 'decimal'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            
            if response.status_code == 200:
                matches_data = response.json()
                
                matches = []
                for match in matches_data:
                    match_info = {
                        'source': 'Odds API',
                        'competition': 'UEFA Champions League',
                        'home_team': match.get('home_team', 'Unknown'),
                        'away_team': match.get('away_team', 'Unknown'),
                        'time': match.get('commence_time', 'Unknown')
                    }
                    matches.append(match_info)
                
                return matches
            else:
                logger.error(f"Odds API error: {response.status_code} - {response.text}")
                return []
        
        except requests.RequestException as e:
            logger.error(f"Odds API network error: {e}")
            return []

    def fetch_api_sports_matches(self, date=None):
        """Fetch matches from API-Sports with robust error handling"""
        try:
            if not self._validate_api_key('api_sports'):
                logger.error("API-Sports key validation failed")
                return []

            date = date or datetime.now().strftime('%Y-%m-%d')
            
            headers = {
                'x-rapidapi-key': self.apis['api_sports']['key'],
                'x-rapidapi-host': 'api-football-v1.p.rapidapi.com'
            }
            
            # Detailed logging for troubleshooting
            logger.info(f"Attempting API-Sports request for date: {date}")
            
            response = requests.get(
                f"{self.apis['api_sports']['base_url']}/fixtures",
                params={'date': date},
                headers=headers
            )
            
            if response.status_code == 200:
                matches_data = response.json().get('response', [])
                parsed_matches = [
                    {
                        'home_team': match.get('teams', {}).get('home', {}).get('name', 'Unknown'),
                        'away_team': match.get('teams', {}).get('away', {}).get('name', 'Unknown'),
                        'datetime': match.get('fixture', {}).get('date', date),
                        'competition': match.get('league', {}).get('name', 'Unknown League')
                    } for match in matches_data
                ]
                logger.info(f"Retrieved {len(parsed_matches)} matches from API-Sports")
                return parsed_matches
            else:
                logger.error(f"API-Sports error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            logger.error(f"[fetch_api_sports_matches] Detailed API-Sports error: {str(e)}")
            return []

    def fetch_matches(self, date=None):
        """Fetch matches from multiple sources with error resilience"""
        all_matches = []
        
        # List of fetch methods to try
        sources = [
            self.fetch_football_data_matches,
            self.fetch_rapidapi_matches,
            self.fetch_sportmonks_matches,
            self.fetch_odds_api_matches,
            self.fetch_api_sports_matches
        ]
        
        for source in sources:
            try:
                matches = source(date)
                all_matches.extend(matches)
            except Exception as e:
                logger.error(f"Error fetching matches from {source.__name__}: {e}")
        
        return all_matches

def main():
    # Allow specifying a date via command line argument
    date_to_fetch = None
    if len(sys.argv) > 1:
        try:
            # Validate date format
            datetime.strptime(sys.argv[1], '%Y-%m-%d')
            date_to_fetch = sys.argv[1]
        except ValueError:
            logger.error(f"Invalid date format. Use YYYY-MM-DD")
            print("Invalid date format. Use YYYY-MM-DD")
            return
    
    # Initialize data sources
    data_sources = FootballDataSources()
    
    # Fetch matches
    matches = data_sources.fetch_matches(date_to_fetch)
    
    if not matches:
        print("No matches found from any sources.")
        logger.info("No matches found from any sources.")
        return
    
    # Print matches
    print(f"Found {len(matches)} matches:")
    for match in matches:
        print(f"[{match['source']}] {match['competition']}: {match['home_team']} vs {match['away_team']} at {match['time']}".encode('utf-8').decode('utf-8'))
    
    # Log matches
    with open('multi_source_matches.log', 'a', encoding='utf-8') as log_file:
        log_file.write(f"\n--- Matches on {datetime.now().strftime('%Y-%m-%d')} ---\n")
        for match in matches:
            log_file.write(f"[{match['source']}] {match['competition']}: {match['home_team']} vs {match['away_team']} at {match['time']}\n")

if __name__ == "__main__":
    main()
