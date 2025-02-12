import os
import requests
from datetime import datetime
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewFootballDataSource:
    def __init__(self):
        load_dotenv()
        self.rapidapi_key = os.getenv('RAPIDAPI_KEY')
        self.base_url = 'https://free-api-live-football-data.p.rapidapi.com'
        
        if not self.rapidapi_key:
            logger.error("RapidAPI key not found in environment variables")
    
    def _get_headers(self):
        """Generate headers for API request"""
        return {
            'X-RapidAPI-Key': self.rapidapi_key,
            'X-RapidAPI-Host': 'free-api-live-football-data.p.rapidapi.com'
        }
    
    def fetch_matches(self, date=None):
        """Fetch football matches for a specific date"""
        date = date or datetime.now().strftime('%Y-%m-%d')
        
        try:
            # Endpoint for fixtures
            endpoint = f'/fixtures/date/{date}'
            
            response = requests.get(
                f'{self.base_url}{endpoint}', 
                headers=self._get_headers()
            )
            
            if response.status_code == 200:
                matches_data = response.json().get('response', [])
                
                parsed_matches = []
                for match in matches_data:
                    try:
                        parsed_match = {
                            'home_team': match.get('teams', {}).get('home', {}).get('name', 'Unknown'),
                            'away_team': match.get('teams', {}).get('away', {}).get('name', 'Unknown'),
                            'datetime': match.get('fixture', {}).get('date', date),
                            'competition': match.get('league', {}).get('name', 'Unknown League')
                        }
                        parsed_matches.append(parsed_match)
                    except Exception as parse_error:
                        logger.warning(f"Error parsing match: {parse_error}")
                
                logger.info(f"Retrieved {len(parsed_matches)} matches")
                return parsed_matches
            else:
                logger.error(f"API request failed: {response.status_code} - {response.text}")
                return []
        
        except requests.RequestException as e:
            logger.error(f"Request error: {e}")
            return []
    
    def verify_api_access(self):
        """Verify API access and get available leagues"""
        try:
            print(f"RapidAPI Key: {self.rapidapi_key[:5]}...{self.rapidapi_key[-5:]}")
            print(f"Base URL: {self.base_url}")
            print(f"Headers: {self._get_headers()}")
            
            response = requests.get(
                f'{self.base_url}/leagues', 
                headers=self._get_headers()
            )
            
            print(f"Response Status: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Content: {response.text[:500]}...")
            
            if response.status_code == 200:
                leagues = response.json().get('response', [])
                logger.info("API Access Verified")
                logger.info(f"Available Leagues: {len(leagues)}")
                
                # Print first 10 leagues for reference
                for league in leagues[:10]:
                    logger.info(f"- {league.get('league', {}).get('name', 'Unknown')}")
                
                return True
            else:
                logger.error(f"API verification failed: {response.status_code}")
                return False
        
        except requests.RequestException as e:
            logger.error(f"Verification error: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False

def main():
    api_source = NewFootballDataSource()
    
    print("Verifying API Access...")
    access_verified = api_source.verify_api_access()
    
    if access_verified:
        print("\nFetching Today's Matches...")
        matches = api_source.fetch_matches()
        
        print("\nMatches Found:")
        for match in matches[:10]:  # Print first 10 matches
            print(f"{match['home_team']} vs {match['away_team']} - {match['competition']}")

if __name__ == "__main__":
    main()
