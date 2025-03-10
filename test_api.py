import os
import json
import logging
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Load environment variables
load_dotenv()

def test_football_data_api():
    """Test the Football-Data.org API with a date range"""
    api_key = os.getenv('FOOTBALL_DATA_API_KEY')
    if not api_key:
        logging.error("Football-Data.org API key not found")
        return

    headers = {'X-Auth-Token': api_key}
    
    # Test with a date range including today and tomorrow
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    url = "https://api.football-data.org/v4/matches"
    params = {
        'dateFrom': today,
        'dateTo': tomorrow
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        print("\nAPI Response Headers:")
        print(f"X-Requests-Available-Minute: {response.headers.get('X-Requests-Available-Minute')}")
        print(f"X-Requests-Available-Day: {response.headers.get('X-Requests-Available-Day')}")
        
        if 'matches' in data:
            matches = data['matches']
            print(f"\nFound {len(matches)} matches for {today} to {tomorrow}")
            
            for match in matches:
                print(f"\nMatch: {match['homeTeam']['name']} vs {match['awayTeam']['name']}")
                print(f"Competition: {match['competition']['name']}")
                print(f"Date: {match['utcDate']}")
                print(f"Status: {match['status']}")
        else:
            print("\nNo matches found in the response")
            print("Full response:", json.dumps(data, indent=2))
            
    except requests.exceptions.RequestException as e:
        print(f"Error testing API: {str(e)}")
        if hasattr(e.response, 'text'):
            print("Error response:", e.response.text)

if __name__ == "__main__":
    test_football_data_api()
