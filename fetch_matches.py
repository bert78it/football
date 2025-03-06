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
            'UEFA Champions League': '🏆',
            'Premier League': '🏴󠁧󠁢󠁥󠁮󠁧󠁿',
            'Serie A': '🇮🇹',
            'La Liga': '🇪🇸',
            'Bundesliga': '🇩🇪',
            'Ligue 1': '🇫🇷',
        }
        
        competition_emoji = emoji_map.get(match.get('competition', ''), '⚽')
        
        message = f"""
🚨 *Upcoming Match Alert!*
{competition_emoji} *{match['home_team']} vs {match['away_team']}*

⏰ Starts in: {time_until_match}
🏆 Competition: {match.get('competition', 'Unknown')}
📅 Date: {match['date']}

_Don't miss this exciting match!_ 🎮
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

def get_google_calendar_service():
    """Gets or creates Google Calendar API service"""
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    creds = None

    if os.path.exists('credentials/token.json'):
        creds = Credentials.from_authorized_user_file('credentials/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('credentials/token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)

def get_calendar_color_id(competition):
    """Get color ID based on competition"""
    color_mapping = {
        'Premier League': '11',  # Red
        'Serie A': '9',         # Green
        'Bundesliga': '5',      # Yellow
        'La Liga': '3',         # Purple
        'Ligue 1': '7',        # Blue
        'Champions League': '1', # Dark Blue
        'Europa League': '2',   # Dark Green
    }
    
    # Try to match competition name with our mapping
    for key in color_mapping:
        if key.lower() in competition.lower():
            return color_mapping[key]
    return '8'  # Gray for other competitions

def create_calendar_file(matches):
    """Create an ICS calendar file with the matches and add to Google Calendar"""
    try:
        cal = Calendar()
        cal.add('version', '2.0')
        cal.add('prodid', '-//Football Matches Calendar//NONSGML v1.0//EN')
        cal.add('calscale', 'GREGORIAN')
        cal.add('method', 'PUBLISH')
        cal.add('x-wr-calname', 'Football Matches')
        cal.add('x-wr-timezone', 'Europe/Rome')
        
        # Get Google Calendar service
        service = get_google_calendar_service()
        
        # Track unique events to avoid duplicates
        unique_events = set()
        
        # Create a list to store matches for notification scheduling
        matches_for_notifications = []
        
        for match in matches:
            event_key = f"{match['home_team']} vs {match['away_team']} - {match['date']}"
            if event_key in unique_events:
                continue
            unique_events.add(event_key)
            
            # Add match to notifications list
            matches_for_notifications.append(match)
            
            # Create ICS event
            ics_event = Event()
            
            # Format title to be more readable
            title = f"⚽ {match['home_team']} vs {match['away_team']}"
            ics_event.add('summary', title)
            
            # Parse the match date
            start_time = datetime.fromisoformat(match['date'].replace('Z', '+00:00'))
            # Set end time to 60 minutes after start (just to mark the start of the match)
            end_time = start_time + timedelta(minutes=60)
            
            ics_event.add('dtstart', start_time)
            ics_event.add('dtend', end_time)
            
            # Add notifications 30 minutes before the match
            alarm_display = Alarm()
            alarm_display.add('action', 'DISPLAY')
            alarm_display.add('description', f"Upcoming match: {match['home_team']} vs {match['away_team']}")
            alarm_display.add('trigger', timedelta(minutes=-30))
            ics_event.add_component(alarm_display)

            alarm_email = Alarm()
            alarm_email.add('action', 'EMAIL')
            alarm_email.add('description', f"Upcoming match: {match['home_team']} vs {match['away_team']}")
            alarm_email.add('trigger', timedelta(minutes=-30))
            alarm_email.add('summary', "Football Match Reminder")
            alarm_email.add('attendee', f"mailto:{os.getenv('RECIPIENT_EMAIL')}")
            ics_event.add_component(alarm_email)
            
            # Add actual match duration in the description
            description = [
                f"🏆 Competition: {match.get('competition', 'Unknown')}",
                f"🏟️ Status: {match.get('status', 'Scheduled')}",
                f"⚽ Full match duration: 105 minutes",
                "",
                "⏰ This event marks the match start time",
                "📅 Calendar Event by Football Matches Daily"
            ]
            description_text = '\n'.join(description)
            ics_event.add('description', description_text)
            
            cal.add_component(ics_event)
            
            # Create Google Calendar event with enhanced formatting
            google_event = {
                'summary': title,
                'description': description_text,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': 'Europe/Rome',
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': 'Europe/Rome',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 60},  # 1 hour before
                        {'method': 'popup', 'minutes': 30},  # 30 minutes before
                        {'method': 'popup', 'minutes': 10},  # 10 minutes before
                    ],
                },
                'colorId': get_calendar_color_id(match.get('competition', '')),
            }
            
            try:
                service.events().insert(calendarId='primary', body=google_event).execute()
                logging.info(f"Added event to Google Calendar: {event_key}")
            except Exception as e:
                logging.error(f"Error adding event to Google Calendar: {str(e)}")
        
        # Schedule notifications for all matches
        asyncio.run(asyncio.gather(*[schedule_match_notifications(match) for match in matches_for_notifications]))
        
        # Write ICS file
        with open('matches.ics', 'wb') as f:
            f.write(cal.to_ical())
        logging.info(f"Created calendar file with {len(unique_events)} unique events")
        
    except Exception as e:
        logging.error(f"Error creating calendar file: {str(e)}")

def fetch_matches():
    """Fetch matches from both APIs and save to file"""
    # Get matches from API-Football
    matches = get_matches_from_api_football()
    
    if not matches:
        logging.warning("No matches found from API-Football, trying Football-Data.org")
        matches = get_matches_from_football_data()
    
    if not matches:
        logging.warning("No matches found from any API")
        matches = []
    
    # Log the number of matches found
    logging.info(f"\nFound {len(matches)} total unique matches:")
    
    # Save matches to JSON file
    with open('matches.json', 'w', encoding='utf-8') as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
    logging.info("Saved matches to matches.json")
    
    # Create calendar file
    create_calendar_file(matches)

if __name__ == "__main__":
    check_env()
    fetch_matches()
