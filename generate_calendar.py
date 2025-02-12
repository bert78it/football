import pytz
from datetime import datetime, timedelta
import ics
import json
import os
import logging
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def load_matches(log_files=None):
    """Load matches from log file."""
    if log_files is None:
        log_files = [
            'football_matches.log', 
            'multi_source_matches.log', 
            'matches.log',
            'fetch_matches_debug.log'
        ]
    
    for log_file in log_files:
        try:
            # Try multiple encodings
            encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(log_file, 'r', encoding=encoding) as f:
                        # Try JSON first
                        try:
                            matches_data = json.load(f)
                            logging.info(f"Loaded matches from {log_file}")
                            return matches_data
                        except json.JSONDecodeError:
                            # Attempt to parse log file for match data
                            f.seek(0)  # Reset file pointer
                            log_content = f.read()
                            import re
                            import ast

                            # Try to find JSON-like match data in the log
                            match_patterns = [
                                r'\{.*?"home_team".*?"away_team".*?"datetime".*?\}',
                                r'\{.*?"homeTeam".*?"awayTeam".*?"date".*?\}'
                            ]
                            
                            matches = []
                            for pattern in match_patterns:
                                found_matches = re.findall(pattern, log_content, re.DOTALL)
                                for match_str in found_matches:
                                    try:
                                        match_dict = ast.literal_eval(match_str)
                                        matches.append(match_dict)
                                    except (SyntaxError, ValueError):
                                        pass
                            
                            if matches:
                                logging.info(f"Extracted {len(matches)} matches from {log_file}")
                                return matches
                            
                            logging.warning(f"Could not parse {log_file} as JSON or extract matches.")
                
                except UnicodeDecodeError:
                    # If current encoding fails, continue to next
                    continue
        
        except FileNotFoundError:
            logging.warning(f"Log file {log_file} not found.")
        except Exception as e:
            logging.error(f"Unexpected error reading {log_file}: {e}")
    
    logging.error("No valid log files found to generate calendar.")
    return []

def create_calendar(matches):
    """Create iCal calendar from matches."""
    calendar = ics.Calendar()
    
    for match in matches:
        try:
            # More robust match parsing
            home_team = match.get('home_team', match.get('homeTeam', 'Unknown Home'))
            away_team = match.get('away_team', match.get('awayTeam', 'Unknown Away'))
            match_time = match.get('datetime', match.get('date', None))
            competition = match.get('competition', match.get('league', 'Football Match'))
            
            if not match_time:
                logging.warning(f"Skipping match without datetime: {match}")
                continue
            
            # Convert to datetime
            match_datetime = datetime.fromisoformat(match_time) if isinstance(match_time, str) else match_time
            match_datetime = match_datetime.replace(tzinfo=pytz.UTC)
            
            # Create calendar event
            event = ics.Event()
            event.name = f"{home_team} vs {away_team}"
            event.description = f"{competition}: {home_team} vs {away_team}"
            event.begin = match_datetime
            event.duration = timedelta(hours=2)  # Typical match duration
            
            calendar.events.add(event)
        except Exception as e:
            logging.error(f"Error processing match: {e}")
    
    return calendar

def save_calendar(calendar, filename='football_matches.ics'):
    """Save calendar to .ics file."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(calendar)
        logging.info(f"Calendar saved to {filename}")
        return True
    except Exception as e:
        logging.error(f"Error saving calendar: {e}")
        return False

import logging
import time
import random
import traceback
from typing import List, Dict, Any

import google.auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure comprehensive logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='google_calendar_debug.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

def exponential_backoff(attempt: int, base_delay: float = 1.0) -> float:
    """
    Calculate exponential backoff with jitter to prevent thundering herd problem.
    
    Args:
        attempt (int): Current retry attempt
        base_delay (float): Base delay in seconds
    
    Returns:
        float: Delay before next retry
    """
    max_delay = 60  # Maximum delay of 1 minute
    delay = min(base_delay * (2 ** attempt) + random.uniform(0, 0.1), max_delay)
    return delay

def get_google_calendar_service():
    """Get Google Calendar service with comprehensive error handling."""
    SCOPES = ['https://www.googleapis.com/auth/calendar.events']
    
    try:
        # Validate credentials file
        if not os.path.exists('credentials.json'):
            logger.error("Credentials file not found!")
            raise FileNotFoundError("credentials.json is missing")

        # OAuth Flow
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        
        # Explicit user consent with local server
        credentials = flow.run_local_server(port=0)
        
        # Save credentials
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())
        
        # Build and return service
        service = build('calendar', 'v3', credentials=credentials)
        return service

    except Exception as e:
        logger.error("Comprehensive Error Tracking:")
        logger.error(f"Error Type: {type(e).__name__}")
        logger.error(f"Error Details: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

def create_event_with_retry(service, match: Dict[str, str], max_attempts: int = 3):
    """
    Create a Google Calendar event with exponential backoff and retry mechanism.
    
    Args:
        service: Google Calendar service
        match (Dict): Match details
        max_attempts (int): Maximum retry attempts
    
    Returns:
        str or None: Event link if successful, None otherwise
    """
    event_title = f"{match['home_team']} vs {match['away_team']} ({match['competition']})"
    
    event = {
        'summary': event_title,
        'start': {
            'dateTime': match['datetime'],
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': match['datetime'],
            'timeZone': 'UTC',
        },
        'description': f"Football match: {event_title}"
    }
    
    for attempt in range(max_attempts):
        try:
            created_event = service.events().insert(
                calendarId='primary', 
                body=event
            ).execute()
            
            logger.info(f"Event created: {created_event.get('htmlLink')}")
            return created_event.get('htmlLink')
        
        except HttpError as e:
            if e.resp.status == 403 and 'rateLimitExceeded' in str(e):
                delay = exponential_backoff(attempt)
                logger.warning(f"Rate limit exceeded. Retrying in {delay:.2f} seconds (Attempt {attempt + 1})")
                time.sleep(delay)
            else:
                logger.error(f"Error creating event for match: {match}")
                logger.error(f"Error details: {str(e)}")
                break
        
        except Exception as e:
            logger.error(f"Unexpected error creating event: {str(e)}")
            break
    
    return None

def upload_to_google_calendar(matches: List[Dict[str, str]], batch_size: int = 10):
    """
    Upload matches to Google Calendar in batches with rate limiting.
    
    Args:
        matches (List[Dict]): List of match details
        batch_size (int): Number of events to create in each batch
    """
    service = get_google_calendar_service()
    
    # Track successful and failed events
    successful_events = []
    failed_events = []
    
    # Process matches in batches
    for i in range(0, len(matches), batch_size):
        batch = matches[i:i+batch_size]
        
        for match in batch:
            event_link = create_event_with_retry(service, match)
            
            if event_link:
                successful_events.append(match)
            else:
                failed_events.append(match)
        
        # Small pause between batches to prevent rate limiting
        time.sleep(1)
    
    # Log summary
    logger.info(f"Batch Upload Summary:")
    logger.info(f"Total Matches: {len(matches)}")
    logger.info(f"Successful Events: {len(successful_events)}")
    logger.info(f"Failed Events: {len(failed_events)}")
    
    # Optional: Save failed events for manual retry
    if failed_events:
        with open('failed_match_events.json', 'w') as f:
            json.dump(failed_events, f, indent=2)
        logger.warning("Some events failed. Check failed_match_events.json")

def main():
    """Main function to load matches and upload to Google Calendar."""
    try:
        # Load matches from log file
        matches = load_matches()
        
        # Upload to Google Calendar
        upload_to_google_calendar(matches)
        
    except Exception as e:
        logger.error(f"Main process error: {str(e)}")
        logger.error(traceback.format_exc())

if __name__ == '__main__':
    main()
