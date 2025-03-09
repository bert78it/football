import os
import json
import logging
import requests
from datetime import datetime, timezone, timedelta
from icalendar import Calendar, Event, Alarm
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from telegram import Bot
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def check_env():
    """Check if required environment variables exist"""
    logging.info("Loading environment variables...")
    required_vars = ['API_FOOTBALL_KEY', 'FOOTBALL_DATA_API_KEY', 'TELEGRAM_BOT_TOKEN', 'RECIPIENT_EMAIL']
    
    for var in required_vars:
        exists = os.getenv(var) is not None
        logging.info(f"{var} present: {exists}")
        if not exists and var != 'TELEGRAM_BOT_TOKEN':
            raise Exception(f"Missing required environment variable: {var}")

# Telegram notification settings
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7847237197:AAHjarLdbbQRAYSTo-iw3iAf3wRT1UEThDw')
TELEGRAM_CHAT_ID = '5819014856'

async def send_telegram_notification(match, time_until_match):
    """Send a notification about an upcoming match via Telegram"""
    try:
        bot = Bot(token=TELEGRAM_BOT_TOKEN)
        
        # Create a nicely formatted message
        emoji_map = {
            # Major European Leagues
            'UEFA Champions League': '🏆',
            'UEFA Europa League': '🌟',
            'UEFA Europa Conference League': '🌍',
            'Premier League': '🏴󠁧󠁢󠁥󠁮󠁧󠁿',
            'Serie A': '🇮🇹',
            'La Liga': '🇪🇸',
            'Bundesliga': '🇩🇪',
            'Ligue 1': '🇫🇷',
            'Eredivisie': '🇳🇱',
            'Primeira Liga': '🇵🇹',
            
            # Domestic Cups
            'FA Cup': '🏆󠁧󠁢󠁥󠁮󠁧󠁿',
            'Coppa Italia': '🏆🇮🇹',
            'Copa del Rey': '🏆🇪🇸',
            'DFB Pokal': '🏆🇩🇪',
            'Coupe de France': '🏆🇫🇷',
            
            # International
            'FIFA World Cup': '🌍',
            'UEFA Euro': '🇪🇺',
            'Copa America': '🏆🌎',
            'Africa Cup of Nations': '🌍',
            'AFC Asian Cup': '🌏',
            
            # Club Competitions
            'FIFA Club World Cup': '🌎',
            'UEFA Super Cup': '🌟',
            'Copa Libertadores': '🏆🌎',
            'Copa Sudamericana': '⭐🌎',
            'AFC Champions League': '🌟🌏'
        }
        
        competition_emoji = emoji_map.get(match.get('competition', ''), '⚽')
        time_emoji = '⏰' if 'hour' in time_until_match else '⚡' if '10 minutes' in time_until_match else '⏳'
        
        message = f"""
{time_emoji} *Upcoming Match Alert!*
{competition_emoji} *{match['home_team']} vs {match['away_team']}*

⏰ Starts in: {time_until_match}
🏆 Competition: {match.get('competition', 'Unknown')}
📅 Date: {match['date']}

_Get ready for kickoff!_ 🎮
        """
        
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message,
            parse_mode='Markdown'
        )
        logging.info(f"Sent Telegram notification for match: {match['home_team']} vs {match['away_team']}")
    except Exception as e:
        logging.error(f"Error sending Telegram notification: {str(e)}")

async def schedule_match_notifications(match):
    """Schedule notifications for a match at different times"""
    match_time = datetime.fromisoformat(match['date'].replace('Z', '+00:00'))
    current_time = datetime.now(timezone.utc)
    
    # Notification times (in minutes before the match)
    notification_times = [60, 30, 10]  # 1 hour, 30 minutes, 10 minutes before
    
    for minutes in notification_times:
        notification_time = match_time - timedelta(minutes=minutes)
        if notification_time > current_time:
            # Calculate wait time
            wait_seconds = (notification_time - current_time).total_seconds()
            if wait_seconds > 0:
                await asyncio.sleep(wait_seconds)
                time_str = f"{minutes} minutes" if minutes != 60 else "1 hour"
                await send_telegram_notification(match, time_str)

async def schedule_notifications(matches):
    """Schedule notifications for all matches"""
    tasks = []
    for match in matches:
        tasks.append(schedule_match_notifications(match))
    await asyncio.gather(*tasks)

def get_matches_from_api_football():
    """Fetch matches from API-Football"""
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    api_key = os.getenv('API_FOOTBALL_KEY')
    
    if not api_key:
        logging.warning("API-Football key not found in environment variables")
        return []

    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }

    # Get today's date in YYYY-MM-DD format
    today = datetime.now().strftime("%Y-%m-%d")
    
    # List of league IDs to fetch
    leagues = [
        135,  # Serie A
        2,    # Champions League
        3,    # Europa League
        39,   # Premier League
        140,  # La Liga
        78,   # Bundesliga
        61,   # Ligue 1
        71,   # Serie B
        848,  # Conference League
        81    # Coppa Italia
    ]
    
    all_matches = []
    seen_matches = set()

    for league in leagues:
        try:
            params = {
                "date": today,
                "league": str(league),
                "timezone": "Europe/Rome"
            }

            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 401:
                logging.error("API-Football error: Invalid API key")
                return []
            response.raise_for_status()
            data = response.json()
            
            if not data.get('response'):
                logging.info(f"No matches found for league {league}")
                continue
                
            for fixture in data.get('response', []):
                match_key = (
                    fixture['teams']['home']['name'],
                    fixture['teams']['away']['name'],
                    fixture['fixture']['date']
                )
                
                if match_key not in seen_matches:
                    seen_matches.add(match_key)
                    match = {
                        'home_team': fixture['teams']['home']['name'],
                        'away_team': fixture['teams']['away']['name'],
                        'date': fixture['fixture']['date'],
                        'venue': fixture['fixture']['venue']['name'] if fixture['fixture'].get('venue') else None,
                        'status': fixture['fixture']['status']['long'],
                        'source': 'API-Football',
                        'competition': fixture['league']['name']
                    }
                    all_matches.append(match)
            
            # Add a small delay between requests to respect rate limits
            import time
            time.sleep(1)
            
        except Exception as e:
            logging.error(f"Error fetching matches for league {league}: {e}")
            continue
    
    logging.info(f"Found {len(all_matches)} matches from API-Football")
    return all_matches

def get_matches_from_football_data():
    """Fetch matches from Football-Data.org"""
    api_key = os.getenv('FOOTBALL_DATA_API_KEY')
    if not api_key:
        logging.warning("Football-Data.org API key not found in environment variables")
        return []

    headers = {'X-Auth-Token': api_key}
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    url = f"http://api.football-data.org/v4/matches?date={today}"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logging.error(f"Error fetching matches from Football-Data.org: {response.status_code}")
            return []

        data = response.json()
        matches = []
        for match in data.get('matches', []):
            # Skip matches without both teams
            if not match.get('homeTeam', {}).get('name') or not match.get('awayTeam', {}).get('name'):
                logging.warning(f"Skipping match with missing team(s): {match.get('homeTeam', {}).get('name', 'Unknown')} vs {match.get('awayTeam', {}).get('name', 'Unknown')}")
                continue
                
            match_data = {
                'home_team': match['homeTeam']['name'],
                'away_team': match['awayTeam']['name'],
                'date': match.get('utcDate'),
                'venue': match.get('venue'),
                'status': match.get('status'),
                'source': 'Football-Data.org',
                'competition': match.get('competition', {}).get('name', 'Unknown Competition')
            }
            matches.append(match_data)

        logging.info(f"Found {len(matches)} matches from Football-Data.org")
        return matches

    except Exception as e:
        logging.error(f"Error fetching matches from Football-Data.org: {str(e)}")
        return []

async def fetch_matches():
    """Fetch matches from both APIs and save to file"""
    check_env()
    
    matches = []
    
    # Try API-Football first
    api_football_matches = get_matches_from_api_football()
    if api_football_matches:
        matches.extend(api_football_matches)
        logging.info(f"Found {len(api_football_matches)} matches from API-Football")
    else:
        logging.warning("No matches found from API-Football, trying Football-Data.org")
        
        # Try Football-Data.org as backup
        football_data_matches = get_matches_from_football_data()
        if football_data_matches:
            matches.extend(football_data_matches)
            logging.info(f"Found {len(football_data_matches)} matches from Football-Data.org")
    
    # Remove duplicates while preserving order
    unique_matches = []
    seen = set()
    for match in matches:
        key = (match['home_team'], match['away_team'], match['date'])
        if key not in seen:
            seen.add(key)
            unique_matches.append(match)
    
    logging.info(f"\nFound {len(unique_matches)} total unique matches:")
    
    # Save matches to file
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(unique_matches, f, indent=2, ensure_ascii=False)
    logging.info("Saved matches to matches.json")
    
    # Schedule notifications for matches
    if unique_matches:
        await schedule_notifications(unique_matches)
        logging.info("Scheduled notifications for matches")
    else:
        logging.warning("No matches to schedule notifications for")

if __name__ == "__main__":
    check_env()
    asyncio.run(fetch_matches())
