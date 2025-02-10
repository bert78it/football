# Football Matches Daily Fetcher

## Project Overview
Automated football match data retrieval from multiple APIs, deployed via GitHub Actions.

## Setup and Deployment

### Local Development
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with API keys:
   ```
   FOOTBALL_DATA_API_KEY=your_key
   RAPIDAPI_KEY=your_key
   SPORTMONKS_API_KEY=your_key
   ODDS_API_KEY=your_key
   API_SPORTS_KEY=your_key
   ```

### GitHub Actions Deployment
1. Fork this repository
2. Go to repository Settings > Secrets
3. Add the following repository secrets:
   - `FOOTBALL_DATA_API_KEY`
   - `RAPIDAPI_KEY`
   - `SPORTMONKS_API_KEY`
   - `ODDS_API_KEY`
   - `API_SPORTS_KEY`

### Workflow Details
- Scheduled daily at 6 AM UTC
- Fetches matches from multiple sources
- Logs results to `multi_source_matches.log`
- Artifacts uploaded for review

## Customization
- Modify `.github/workflows/fetch_matches.yml` to change schedule
- Update `multi_source_matches.py` to add/remove data sources

## Output
Matches are logged and can be retrieved as workflow artifacts.
