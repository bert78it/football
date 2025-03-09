# Football Match Notifications

## Overview
Automatically fetches football matches from multiple sources and sends notifications via Telegram. Running entirely in the cloud via GitHub Actions, no local machine needed!

## Features
- Fetches matches from Football-Data.org and API-Football
- Smart Telegram notifications:
  - 1 hour before match
  - 30 minutes before match
  - 10 minutes before match
- Beautiful emoji-enhanced notifications 🎮
- Runs automatically in the cloud via GitHub Actions
- Timezone-aware (configured for Rome time)
- No need to keep your PC running

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
   - `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
   - `RECIPIENT_EMAIL`: Your email (for future features)

## Automation
The script runs automatically via GitHub Actions:
- Three times daily (6:00, 12:00, and 18:00 Rome time)
- Fetches upcoming matches
- Sends Telegram notifications before each match
- Runs entirely in the cloud - no local machine needed!

## Notification Format
You'll receive beautifully formatted notifications like this:
```
⚡ Upcoming Match Alert!
🇪🇸 Real Madrid vs Barcelona

⏰ Starts in: 30 minutes
🏆 Competition: La Liga
📅 Date: 2025-03-09 20:00

Get ready for kickoff! 🎮
```

## Troubleshooting
- Check GitHub Actions logs for any errors
- Verify all secrets are correctly set in GitHub
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
   RECIPIENT_EMAIL=your_email
   ```
4. Run: `python fetch_matches.py`

## Testing
The repository includes two utility scripts:
- `verify_setup.py`: Verifies your environment setup and Telegram bot
- `send_test_notification.py`: Sends a test match notification

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
