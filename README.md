# Football Matches Daily Calendar

## Overview
Automatically fetches football matches from multiple sources and adds them to your Google Calendar with Telegram notifications.

## Features
- Fetches matches from Football-Data.org and API-Football
- Automatically adds matches to Google Calendar
- Multiple notification channels:
  - Telegram notifications (1 hour, 30 minutes, and 10 minutes before matches)
  - Google Calendar notifications
- Color-coded events based on competition
- 60-minute event duration for better calendar visualization
- Runs daily via GitHub Actions
- Beautiful emoji-enhanced notifications 🎮

## Setup

### 1. API Keys
You need API keys from:
- Football-Data.org
- API-Football

### 2. Telegram Bot Setup
1. Create a new Telegram bot:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Use the `/newbot` command and follow instructions
   - Save your bot token (looks like `123456789:ABCdefGHIjklmNOPQrstUVwxyz`)

2. Get your chat ID:
   - Message your bot
   - Visit `https://api.telegram.org/bot<YourBOTToken>/getUpdates`
   - Look for `"chat":{"id":123456789}`

### 3. GitHub Repository Setup
1. Fork this repository
2. Go to repository Settings > Secrets and variables > Actions
3. Add the following repository secrets:
   - `FOOTBALL_DATA_API_KEY`: Your Football-Data.org API key
   - `API_FOOTBALL_KEY`: Your API-Football key
   - `GOOGLE_CALENDAR_TOKEN`: Your Google Calendar OAuth token (JSON format)
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
   - `TELEGRAM_CHAT_ID`: Your Telegram chat ID

### 4. Google Calendar Integration
The script will automatically:
- Add matches to your primary Google Calendar
- Set notifications at 1 hour, 30 minutes, and 10 minutes before each match
- Color-code events based on competition
- Set 60-minute duration for each match event

## Automation
- GitHub Actions workflow runs daily at 11:00 UTC
- Fetches matches and adds them to your calendar automatically
- Sends Telegram notifications for upcoming matches
- No manual intervention needed once set up

## Troubleshooting
- Check GitHub Actions logs for any errors
- Verify all secrets are correctly set in GitHub
- Ensure Google Calendar token is up to date
- For Telegram issues:
  - Check if your bot token is valid
  - Ensure you've messaged your bot at least once
  - Verify your chat ID is correct

## Development
To run locally:
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file with your API keys:
   ```
   FOOTBALL_DATA_API_KEY=your_key
   API_FOOTBALL_KEY=your_key
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```
4. Run: `python fetch_matches.py`

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

*Last Updated: March 2025*

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Support the Project

If you find this project helpful, consider supporting its development:

<a href="https://www.buymeacoffee.com/bert78it" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
