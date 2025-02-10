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

## Legal Disclaimer and Acceptable Use

### 🚨 Important Notice

**THIS SOFTWARE IS PROVIDED FOR EDUCATIONAL AND PERSONAL USE ONLY**

#### Prohibited Uses
- **Do NOT use this script for:**
  - IPTV streaming
  - Unauthorized content redistribution
  - Copyright infringement
  - Commercial exploitation of match data
  - Any illegal or unethical purposes

#### Liability and Responsibility
- The creator of this script assumes NO responsibility for:
  - Misuse of the software
  - Legal consequences arising from improper use
  - Any damages or losses incurred
  - Violations of terms of service of data providers

#### User Acknowledgment
By using this script, you explicitly agree that:
1. You will use the data only for personal, non-commercial purposes
2. You understand and accept full legal responsibility for your actions
3. You will comply with all applicable laws and API providers' terms of service

**Violation of these terms may result in legal action and immediate revocation of usage rights.**

*Last Updated: February 2025*

## Support the Project

If you find this project helpful, consider supporting its development:

<a href="https://www.buymeacoffee.com/bert78it" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
