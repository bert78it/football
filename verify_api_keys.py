import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def verify_football_data_api():
    """Verify Football-Data.org API key"""
    api_key = os.getenv('FOOTBALL_DATA_API_KEY')
    if not api_key:
        print("Football-Data.org API key not found")
        return False
    
    headers = {'X-Auth-Token': api_key}
    try:
        response = requests.get(
            'https://api.football-data.org/v4/competitions', 
            headers=headers
        )
        if response.status_code == 200:
            print("Football-Data.org API key is valid")
            return True
        else:
            print(f"Football-Data.org API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"Football-Data.org API verification failed: {e}")
        return False

def verify_rapidapi():
    """Verify RapidAPI key"""
    api_key = os.getenv('RAPIDAPI_KEY')
    if not api_key:
        print("RapidAPI key not found")
        return False
    
    headers = {
        'X-RapidAPI-Key': api_key,
        'X-RapidAPI-Host': 'api-football-v1.p.rapidapi.com'
    }
    try:
        response = requests.get(
            'https://api-football-v1.p.rapidapi.com/v3/leagues', 
            headers=headers
        )
        if response.status_code == 200:
            print("RapidAPI key is valid")
            return True
        else:
            print(f"RapidAPI error: {response.status_code}")
            return False
    except Exception as e:
        print(f"RapidAPI verification failed: {e}")
        return False

def verify_sportmonks_api():
    """Verify SportMonks API key"""
    api_key = os.getenv('SPORTMONKS_API_KEY')
    if not api_key:
        print("SportMonks API key not found")
        return False
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
    try:
        response = requests.get(
            'https://api.sportmonks.com/v3/leagues', 
            headers=headers
        )
        if response.status_code == 200:
            print("SportMonks API key is valid")
            return True
        else:
            print(f"SportMonks API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"SportMonks API verification failed: {e}")
        return False

def verify_odds_api():
    """Verify Odds API key"""
    api_key = os.getenv('ODDS_API_KEY')
    if not api_key:
        print("Odds API key not found")
        return False
    
    try:
        response = requests.get(
            f'https://api.the-odds-api.com/v4/sports', 
            params={'apiKey': api_key}
        )
        if response.status_code == 200:
            print("Odds API key is valid")
            return True
        else:
            print(f"Odds API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"Odds API verification failed: {e}")
        return False

def verify_api_sports():
    """Verify API-Sports key"""
    api_key = os.getenv('API_SPORTS_KEY')
    if not api_key:
        print("API-Sports key not found")
        return False
    
    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    try:
        response = requests.get(
            'https://v3.football.api-sports.io/leagues', 
            headers=headers
        )
        if response.status_code == 200:
            print("API-Sports key is valid")
            return True
        else:
            print(f"API-Sports error: {response.status_code}")
            return False
    except Exception as e:
        print(f"API-Sports verification failed: {e}")
        return False

def main():
    print("Verifying API Keys:")
    apis = [
        verify_football_data_api,
        verify_rapidapi,
        verify_sportmonks_api,
        verify_odds_api,
        verify_api_sports
    ]
    
    valid_apis = sum(api() for api in apis)
    print(f"\nSummary: {valid_apis}/{len(apis)} APIs verified")

if __name__ == "__main__":
    main()
