# Google Calendar API Setup Guide

## Prerequisites
- Python 3.7+
- Google Account
- Google Cloud Project

## Step-by-Step Setup

### 1. Create a Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Create Project"
3. Name your project (e.g., "Football Matches Calendar")
4. Select the project

### 2. Enable Google Calendar API
1. In the Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google Calendar API"
3. Click "Enable"

### 3. Create OAuth 2.0 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Desktop app" as the application type
4. Name your OAuth 2.0 client (e.g., "Football Matches Desktop")
5. Click "Create"
6. Download the client configuration
7. Rename the downloaded file to `credentials.json`
8. Place `credentials.json` in this project directory

### 4. First-Time Authorization
When you first run `generate_calendar.py`:
- A browser window will open
- Select the Google account you want to use
- Grant permissions to access Google Calendar
- A `token.json` will be automatically created for future use

### Troubleshooting
- If you want to use a different Google account, delete `token.json`
- Ensure `credentials.json` is in the same directory as the script
- Check that you have the latest versions of `google-api-python-client` and `google-auth-oauthlib`

## Security Notes
- Never commit `credentials.json` or `token.json` to version control
- Keep these files private and secure
