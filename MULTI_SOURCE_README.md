# Multi-Source Football Matches Fetcher

## Features
- Fetch football matches from multiple API sources
- Flexible date selection
- Comprehensive logging
- Easy to extend with new data sources

## Prerequisites
- Python 3.8+
- API keys (optional)

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Optional: Configure API Keys
   - For football-data.org:
     Set `FOOTBALL_DATA_API_KEY` in `.env`
   - For RapidAPI:
     Set `RAPIDAPI_KEY` and `RAPIDAPI_HOST` in `.env`

## Running the Script
```bash
# Fetch matches for today
python multi_source_matches.py

# Fetch matches for a specific date
python multi_source_matches.py 2024-02-15
```

## Adding New Data Sources

### Step-by-Step Guide

1. **Obtain API Credentials**
   - Sign up for the football data API
   - Get your API key
   - Review the API documentation

2. **Create a New Fetch Method**
   ```python
   def fetch_new_api_matches(self, date=None):
       # Check API key
       if not self.new_api_key:
           logging.warning("No New API key provided")
           return []

       date = date or datetime.now().strftime('%Y-%m-%d')
       
       try:
           # Make API request
           response = requests.get(api_url, headers=headers)
           
           if response.status_code == 200:
               matches = []
               for match in response.json().get('matches', []):
                   match_info = {
                       'source': 'New API',
                       'competition': match.get('league', 'Unknown'),
                       'home_team': match.get('home_team', 'Unknown'),
                       'away_team': match.get('away_team', 'Unknown'),
                       'time': match.get('time', 'Unknown')
                   }
                   matches.append(match_info)
               
               return matches
           
       except Exception as e:
           logging.error(f"New API fetch error: {e}")
           return []
   ```

3. **Update Fetch Method**
   ```python
   def fetch_matches(self, date=None):
       all_matches = []
       all_matches.extend(self.fetch_football_data_matches(date))
       all_matches.extend(self.fetch_new_api_matches(date))
       return all_matches
   ```

### Best Practices
- Always handle potential API errors
- Use consistent match information format
- Add API key to `.env` file
- Log errors for debugging
- Handle rate limits and quotas

## Logging
- Matches are logged to `multi_source_matches.log`
- Includes source, competition, teams, and match time

## Extending
- Add new data sources by creating methods in the `FootballDataSources` class
- Implement parsing logic specific to each API's response structure

## Troubleshooting
- Check `.env` file for correct API keys
- Review `multi_source_matches.log` for detailed logs
- Ensure stable internet connection
