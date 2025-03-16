import os

def sanitize_env_var(value):
    """Sanitizza una variabile rimuovendo spazi e newline"""
    def sanitize_env_var(env_var: str) -> str:
    return ''.join(filter(lambda x: x.isprintable() and x != '\n', env_var)).strip() if env_var else ''


def load_and_sanitize_env_vars():
    """Carica e sanitizza tutte le variabili d'ambiente richieste"""
    env_vars = {
        telegram_bot_token = sanitize_env_var(os.getenv('TELEGRAM_BOT_TOKEN'))
        telegram_chat_id = sanitize_env_var(os.getenv('TELEGRAM_CHAT_ID'))print(f"Sanitized TELEGRAM_BOT_TOKEN: {repr(telegram_bot_token)}")
print(f"Sanitized TELEGRAM_CHAT_ID: {repr(telegram_chat_id)}")


        "FOOTBALL_DATA_API_KEY": sanitize_env_var(os.getenv('FOOTBALL_DATA_API_KEY')),
    }
    # Log per debug (assicurati di rimuovere in produzione!)
    for key, value in env_vars.items():
        print(f"Sanitized {key}: {repr(value)}")
    return env_vars

from dotenv import load_dotenv
import os

# Carica il file .env
load_dotenv()

# Stampa per verificare le variabili
print("TELEGRAM_BOT_TOKEN:", repr(os.getenv('TELEGRAM_BOT_TOKEN')))
print("TELEGRAM_CHAT_ID:", repr(os.getenv('TELEGRAM_CHAT_ID')))
print("FOOTBALL_DATA_API_KEY:", repr(os.getenv('FOOTBALL_DATA_API_KEY')))

# Esempio di utilizzo
env_vars = load_and_sanitize_env_vars()
telegram_bot_token = env_vars["TELEGRAM_BOT_TOKEN"]
telegram_chat_id = env_vars["TELEGRAM_CHAT_ID"]
football_data_api_key = env_vars["FOOTBALL_DATA_API_KEY"]


import os

telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

# Stampa il valore con `repr` per evidenziare eventuali caratteri non visibili
print(f"Valore originale del token: {repr(telegram_bot_token)}")

import logging
import requests
import os

# Funzione per sanitizzare le variabili
def sanitize_env_var(env_var: str) -> str:
    return ''.join(filter(lambda x: x.isprintable(), env_var)).strip()

def send_telegram_message(message: str) -> None:
    telegram_bot_token = sanitize_env_var(os.getenv('TELEGRAM_BOT_TOKEN'))
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {"chat_id": sanitize_env_var(os.getenv('TELEGRAM_CHAT_ID')), "text": message}

    try:
        response = requests.post(url, json=payload)
        logging.info(f"Constructed URL: {url}")
        logging.info(f"Payload: {payload}")
        logging.info(f"Response Code: {response.status_code}")
        logging.info(f"Response Text: {response.text}")

        if response.status_code != 200:
            logging.error(f"Failed to send message: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        logging.error(f"Exception during Telegram API call: {e}")

# Verifica e stampa le variabili di ambiente
telegram_chat_id = sanitize_env_var(os.getenv('TELEGRAM_CHAT_ID'))
telegram_bot_token = sanitize_env_var(os.getenv('TELEGRAM_BOT_TOKEN'))
football_data_api_key = sanitize_env_var(os.getenv('FOOTBALL_DATA_API_KEY'))

logging.info("Sanitized TELEGRAM_CHAT_ID: %s", telegram_chat_id)
logging.info("Sanitized TELEGRAM_BOT_TOKEN: %s", telegram_bot_token)
logging.info("Sanitized FOOTBALL_DATA_API_KEY: %s", football_data_api_key)



if not telegram_chat_id:
    raise Exception("Missing required environment variable: TELEGRAM_CHAT_ID")
if not telegram_bot_token:
    raise Exception("Missing required environment variable: TELEGRAM_BOT_TOKEN")
if not football_data_api_key:
    raise Exception("Missing required environment variable: FOOTBALL_DATA_API_KEY")

print("Sanitized TELEGRAM_CHAT_ID:", telegram_chat_id)
print("Sanitized TELEGRAM_BOT_TOKEN:", telegram_bot_token)
print("Sanitized FOOTBALL_DATA_API_KEY:", football_data_api_key)



print("TELEGRAM_CHAT_ID:", telegram_chat_id)
print("TELEGRAM_BOT_TOKEN:", telegram_bot_token)
print("FOOTBALL_DATA_API_KEY:", football_data_api_key)

# Esempio di richiesta all'API di Telegram
telegram_api_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
print(f"URL sanitizzato: {repr(url)}")

params = {
    "chat_id": telegram_chat_id,
    "text": "Il calendario delle partite di oggi è pronto!"
}
response = requests.get(telegram_api_url, params=params)
print(response.json())

import os
import requests

# Stampa i valori delle variabili di ambiente
print("TELEGRAM_CHAT_ID:", os.getenv('TELEGRAM_CHAT_ID'))
print("TELEGRAM_BOT_TOKEN:", os.getenv('TELEGRAM_BOT_TOKEN'))
print("FOOTBALL_DATA_API_KEY:", os.getenv('FOOTBALL_DATA_API_KEY'))
print(f"Sanitized TELEGRAM_BOT_TOKEN: {repr(telegram_bot_token)}")
print(f"Sanitized TELEGRAM_CHAT_ID: {repr(telegram_chat_id)}")
print(f"Original TELEGRAM_BOT_TOKEN: {repr(os.getenv('TELEGRAM_BOT_TOKEN'))}")
print(f"Original TELEGRAM_CHAT_ID: {repr(os.getenv('TELEGRAM_CHAT_ID'))}")



# Codice esistente...
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
import time  # Import time module

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
    required_vars = ['FOOTBALL_DATA_API_KEY', 'TELEGRAM_BOT_TOKEN', 'TELEGRAM_CHAT_ID', 'RECIPIENT_EMAIL']
    
    for var in required_vars:
        exists = os.getenv(var) is not None
        logging.info(f"{var} present: {exists}")
        if not exists and var != 'TELEGRAM_BOT_TOKEN':
            raise Exception(f"Missing required environment variable: {var}")

# Telegram notification settings
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

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
            'Premier League': '🏴',
            'Serie A': '🇮🇹',
            'La Liga': '🇪🇸',
            'Bundesliga': '🇩🇪',
            'Ligue 1': '🇫🇷',
            'Eredivisie': '🇳🇱',
            'Primeira Liga': '🇵🇹',
            
            # Domestic Cups
            'FA Cup': '🏆',
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
        
        # Add rate limiting
        for _ in range(10):  # Assuming you need to make 10 calls
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
            
            # Respect rate limit
            time.sleep(6)  # Sleep for 6 seconds to ensure 10 calls per minute
            
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
