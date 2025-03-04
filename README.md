# Football Matches Daily Calendar

## Overview
Automatically fetches football matches from multiple sources and adds them to your Google Calendar with notifications.

## Features
- Fetches matches from Football-Data.org and API-Football
- Automatically adds matches to Google Calendar
- Multiple notifications (1 hour, 30 minutes, and 10 minutes before each match)
- Color-coded events based on competition
- 60-minute event duration for better calendar visualization
- Runs daily via GitHub Actions

## Setup

### 1. API Keys
You need API keys from:
- Football-Data.org
- API-Football

### 2. GitHub Repository Setup
1. Fork this repository
2. Go to repository Settings > Secrets and variables > Actions
3. Add the following repository secrets:
   - `FOOTBALL_DATA_API_KEY`: Your Football-Data.org API key
   - `API_FOOTBALL_KEY`: Your API-Football key
   - `GOOGLE_CALENDAR_TOKEN`: Your Google Calendar OAuth token (JSON format)

### 3. Google Calendar Integration
The script will automatically:
- Add matches to your primary Google Calendar
- Set notifications at 1 hour, 30 minutes, and 10 minutes before each match
- Color-code events based on competition
- Set 60-minute duration for each match event

## Automation
- GitHub Actions workflow runs daily at 11:00 UTC
- Fetches matches and adds them to your calendar automatically
- No manual intervention needed once set up

## Troubleshooting
- Check GitHub Actions logs for any errors
- Verify all secrets are correctly set in GitHub
- Ensure Google Calendar token is up to date

## Development
To run locally:
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your API keys:
   ```
   FOOTBALL_DATA_API_KEY=your_key
   API_FOOTBALL_KEY=your_key
   ```
4. Run: `python fetch_matches.py`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Support the Project

If you find this project helpful, consider supporting its development:

<a href="https://www.buymeacoffee.com/bert78it" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
