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
                'base_url': 'https://football-live-data.p.rapidapi.com',
                'rate_limit': 30  # requests per minute
            },
            'api_sports': {
                'key': os.getenv('API_SPORTS_KEY', ''),
                'base_url': 'https://v3.football.api-sports.io',
                'rate_limit': 30  # requests per minute
            },
            'api_football': {
                'key': os.getenv('API_FOOTBALL_KEY', ''),
                'base_url': 'https://api-football-v1.p.rapidapi.com/v3',
                'rate_limit': 20  # requests per minute
            },
            'odds_api': {
                'key': os.getenv('ODDS_API_KEY', ''),
                'base_url': 'https://api.the-odds-api.com/v4/sports/soccer_uefa_champs_league/odds',
                'rate_limit': 10  # requests per minute
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
        """Fetch matches from Football-Data.org with robust error handling"""
        try:
            if not self._validate_api_key('football_data'):
                logger.error("Football-Data.org key validation failed")
                return []

            date = date or datetime.now().strftime('%Y-%m-%d')
            
            headers = {
                'X-Auth-Token': self.apis['football_data']['key']
            }
            
            # Detailed logging for troubleshooting
            logger.info(f"Attempting Football-Data.org request for date: {date}")
            
            response = requests.get(
                f"{self.apis['football_data']['base_url']}/matches",
                params={'dateFrom': date, 'dateTo': date},
                headers=headers
            )
            
            if response.status_code == 200:
                matches_data = response.json().get('matches', [])
                parsed_matches = [
                    {
                        'home_team': match.get('homeTeam', {}).get('name', 'Unknown'),
                        'away_team': match.get('awayTeam', {}).get('name', 'Unknown'),
                        'datetime': match.get('utcDate', date),
                        'competition': match.get('competition', {}).get('name', 'Unknown League'),
                        'source': 'Football-Data.org'  # Add source key
                    } for match in matches_data
                ]
                logger.info(f"Retrieved {len(parsed_matches)} matches from Football-Data.org")
                return parsed_matches
            else:
                logger.error(f"Football-Data.org API error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            logger.error(f"[fetch_football_data_matches] Detailed Football-Data.org error: {str(e)}")
            return []

    def fetch_rapidapi_matches(self, date=None):
        """Fetch matches from RapidAPI with robust error handling"""
        try:
            if not self._validate_api_key('rapidapi'):
                logger.error("RapidAPI key validation failed")
                return []

            date = date or datetime.now().strftime('%Y-%m-%d')
            
            headers = {
                'X-RapidAPI-Key': self.apis['rapidapi']['key'],
                'X-RapidAPI-Host': 'football-live-data.p.rapidapi.com'
            }
            
            # Detailed logging for troubleshooting
            logger.info(f"Attempting RapidAPI request for date: {date}")
            
            response = requests.get(
                f"{self.apis['rapidapi']['base_url']}/fixtures",
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
                        'competition': match.get('league', {}).get('name', 'Unknown League'),
                        'source': 'RapidAPI'  # Add source key
                    } for match in matches_data
                ]
                logger.info(f"Retrieved {len(parsed_matches)} matches from RapidAPI")
                return parsed_matches
            else:
                logger.error(f"RapidAPI error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            logger.error(f"[fetch_rapidapi_matches] Detailed RapidAPI error: {str(e)}")
            return []

    def fetch_api_football_matches(self, date=None):
        """Fetch matches from API-Football with robust error handling"""
        try:
            if not self._validate_api_key('api_football'):
                logger.error("API-Football key validation failed")
                return []

            date = date or datetime.now().strftime('%Y-%m-%d')
            
            headers = {
                'X-RapidAPI-Key': self.apis['api_football']['key'],
                'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com'
            }
            
            # Detailed logging for troubleshooting
            logger.info(f"Attempting API-Football request for date: {date}")
            
            response = requests.get(
                f"{self.apis['api_football']['base_url']}/fixtures",
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
                        'competition': match.get('league', {}).get('name', 'Unknown League'),
                        'source': 'API-Football'  # Add source key
                    } for match in matches_data
                ]
                logger.info(f"Retrieved {len(parsed_matches)} matches from API-Football")
                return parsed_matches
            else:
                logger.error(f"API-Football error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            logger.error(f"[fetch_api_football_matches] Detailed API-Football error: {str(e)}")
            return []

    def fetch_odds_api_matches(self, date=None):
        """Fetch matches from Odds API with robust error handling"""
        try:
            if not self._validate_api_key('odds_api'):
                logger.error("Odds API key validation failed")
                return []

            date = date or datetime.now().strftime('%Y-%m-%d')
            
            headers = {
                'X-API-Key': self.apis['odds_api']['key']
            }
            
            # Detailed logging for troubleshooting
            logger.info(f"Attempting Odds API request for date: {date}")
            
            response = requests.get(
                f"{self.apis['odds_api']['base_url']}/odds",
                params={'date': date},
                headers=headers
            )
            
            if response.status_code == 200:
                matches_data = response.json().get('data', [])
                parsed_matches = [
                    {
                        'home_team': match.get('teams', [])[0],
                        'away_team': match.get('teams', [])[1],
                        'datetime': match.get('commence_time', date),
                        'competition': match.get('sport_key', 'Unknown League'),
                        'source': 'Odds API'  # Add source key
                    } for match in matches_data
                ]
                logger.info(f"Retrieved {len(parsed_matches)} matches from Odds API")
                return parsed_matches
            else:
                logger.error(f"Odds API error: {response.status_code} - {response.text}")
                return []
        except Exception as e:
            logger.error(f"[fetch_odds_api_matches] Detailed Odds API error: {str(e)}")
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
                'x-rapidapi-host': 'v3.football.api-sports.io'
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
                        'competition': match.get('league', {}).get('name', 'Unknown League'),
                        'source': 'API-Sports'  # Add source key
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
        """
        Fetch matches from multiple sources with fallback strategy
        Prioritize sources based on reliability and coverage
        """
        date = date or datetime.now().strftime('%Y-%m-%d')
        
        # Prioritized API sources
        api_sources = [
            self.fetch_rapidapi_matches,  # Most reliable
            self.fetch_odds_api_matches,  # Secondary source
            self.fetch_football_data_matches,  # Tertiary sources
            self.fetch_api_football_matches,
            self.fetch_api_sports_matches
        ]
        
        all_matches = []
        for source in api_sources:
            try:
                matches = source(date)
                if matches:
                    logger.info(f"Retrieved {len(matches)} matches from {source.__name__}")
                    all_matches.extend(matches)
            except Exception as e:
                logger.warning(f"Error fetching matches from {source.__name__}: {e}")
        
        # Remove duplicates while preserving order
        unique_matches = []
        seen = set()
        for match in all_matches:
            match_key = (match.get('home_team'), match.get('away_team'), match.get('datetime'))
            if match_key not in seen:
                seen.add(match_key)
                unique_matches.append(match)
        
        logger.info(f"Total unique matches retrieved: {len(unique_matches)}")
        return unique_matches

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
        print(f"[{match['source']}] {match['competition']}: {match['home_team']} vs {match['away_team']} at {match['datetime']}".encode('utf-8').decode('utf-8'))
    
    # Log matches
    with open('multi_source_matches.log', 'a', encoding='utf-8') as log_file:
        log_file.write(f"\n--- Matches on {datetime.now().strftime('%Y-%m-%d')} ---\n")
        for match in matches:
            log_file.write(f"[{match['source']}] {match['competition']}: {match['home_team']} vs {match['away_team']} at {match['datetime']}\n")

if __name__ == "__main__":
    main()
