import os
import sys
import requests
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables faster
load_dotenv(override=True)

# Configure logging with minimal overhead
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for more information
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='football_matches.log',
    filemode='a',
    force=True
)

# Get API key directly and cache it
API_KEY = os.getenv('FOOTBALL_DATA_API_KEY', '')

def fetch_matches(date=None):
    """
    Fetch matches for a specific date with optimized performance
    """
    if not API_KEY:
        logging.error("No API key provided")
        print("Error: No API key provided")
        return []

    # Use current date if no date provided
    date = date or datetime.now().strftime('%Y-%m-%d')
    
    try:
        # Optimize headers and use a timeout
        headers = {
            'X-Auth-Token': API_KEY,
            'Accept': 'application/json'
        }
        
        # Simplified URL with minimal parameters
        url = f'https://api.football-data.org/v4/matches?dateFrom={date}&dateTo={date}'
        logging.debug(f"Requesting URL: {url}")
        
        # Use a reasonable timeout to prevent hanging
        response = requests.get(url, headers=headers, timeout=10)
        
        logging.debug(f"Response status code: {response.status_code}")
        logging.debug(f"Response headers: {response.headers}")
        
        # Quick early exit for non-200 responses
        if response.status_code != 200:
            logging.error(f"API request failed: {response.status_code}")
            logging.error(f"Response content: {response.text}")
            print(f"API request failed: {response.status_code}")
            return []
        
        # Minimal parsing
        matches_data = response.json().get('matches', [])
        
        logging.debug(f"Total matches found: {len(matches_data)}")
        
        # Lightweight match processing
        matches = []
        for match in matches_data:
            match_info = {
                'competition': match.get('competition', {}).get('name', 'Unknown'),
                'home_team': match.get('homeTeam', {}).get('name', 'Unknown'),
                'away_team': match.get('awayTeam', {}).get('name', 'Unknown'),
                'time': match.get('utcDate', 'Unknown')
            }
            matches.append(match_info)
        
        return matches
    
    except requests.RequestException as e:
        logging.error(f"Network error: {e}")
        print(f"Network error: {e}")
        return []
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
        return []

def main():
    try:
        # Allow specifying a date via command line argument
        date_to_fetch = None
        if len(sys.argv) > 1:
            date_to_fetch = sys.argv[1]
        
        # Fetch and log matches
        matches = fetch_matches(date_to_fetch)
        
        if not matches:
            print("No matches found or error occurred.")
            return
        
        # Compact logging and printing
        print(f"Found {len(matches)} matches:")
        for match in matches:
            print(f"- {match['competition']}: {match['home_team']} vs {match['away_team']} at {match['time']}")
        
        # Optional: Log to file
        with open('football_matches.log', 'a') as log_file:
            log_file.write(f"\n--- Matches on {datetime.now().strftime('%Y-%m-%d')} ---\n")
            for match in matches:
                log_file.write(f"{match['competition']}: {match['home_team']} vs {match['away_team']} at {match['time']}\n")
    
    except Exception as e:
        logging.error(f"Main execution error: {e}")

if __name__ == "__main__":
    main()
