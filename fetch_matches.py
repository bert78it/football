import os
import json
import logging
from logging.handlers import RotatingFileHandler
import requests
from datetime import datetime, timezone, timedelta
from telegram import Bot
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Enable logging
log_file = 'football_notifications.log'
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),  # Console output
        RotatingFileHandler(
            log_file,
            maxBytes=1024*1024,  # 1MB
            backupCount=5,
            encoding='utf-8'
        )
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def check_env():
    """Check if required environment variables exist"""
    logging.info("Loading environment variables...")
    required_vars = ['FOOTBALL_DATA_API_KEY', 'TELEGRAM_BOT_TOKEN', 'RECIPIENT_EMAIL']
    
    for var in required_vars:
        exists = os.getenv(var) is not None
        logging.info(f"{var} present: {exists}")
        if not exists and var != 'TELEGRAM_BOT_TOKEN':
            raise Exception(f"Missing required environment variable: {var}")

# Telegram notification settings
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
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

def get_matches_from_football_data():
    """Fetch matches from Football-Data.org"""
    api_key = os.getenv('FOOTBALL_DATA_API_KEY')
    if not api_key:
        logging.error("Football-Data.org API key not found")
        return []

    headers = {'X-Auth-Token': api_key}
    
    # Get today's date and tomorrow's date
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    all_matches = []
    
    try:
        # Fetch matches for today and tomorrow
        url = f"https://api.football-data.org/v4/matches"
        params = {'dateFrom': today, 'dateTo': tomorrow}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'matches' in data:
            for match in data['matches']:
                match_info = {
                    'home_team': match['homeTeam']['name'],
                    'away_team': match['awayTeam']['name'],
                    'date': match['utcDate'],
                    'competition': match['competition']['name'],
                    'status': match['status'],
                    'source': 'Football-Data.org'
                }
                all_matches.append(match_info)
            
            logging.info(f"Found {len(all_matches)} matches from Football-Data.org")
        else:
            logging.warning("No matches found in the response")
            
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching matches from Football-Data.org: {str(e)}")
    
    return all_matches

async def fetch_matches():
    """Main function to fetch matches and schedule notifications"""
    try:
        # Fetch matches from Football-Data.org
        matches = get_matches_from_football_data()
        logging.info(f"Found {len(matches)} total unique matches")
        
        # Save matches to file for reference
        with open('matches.json', 'w', encoding='utf-8') as f:
            json.dump(matches, f, ensure_ascii=False, indent=2)
        logging.info("Saved matches to matches.json")
        
        # Schedule notifications for matches
        logging.info("Scheduled notifications for matches")
        await schedule_notifications(matches)
        
    except Exception as e:
        logging.error(f"Error in fetch_matches: {str(e)}")

if __name__ == "__main__":
    check_env()
    asyncio.run(fetch_matches())
