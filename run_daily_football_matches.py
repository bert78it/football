import os
import sys
import logging
from datetime import datetime, timedelta

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our custom modules
import fetch_matches
import generate_calendar

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    filename='daily_football_automation.log'
)

def main():
    try:
        # Log the start of the daily automation
        logging.info("Starting daily football matches automation")

        # Fetch matches for the next 7 days
        matches = fetch_matches.fetch_upcoming_matches(days_ahead=7)
        
        if not matches:
            logging.warning("No matches found for the upcoming week")
            return

        # Upload matches to Google Calendar
        generate_calendar.upload_to_google_calendar(matches)
        
        # Log successful completion
        logging.info(f"Successfully processed and uploaded {len(matches)} matches to Google Calendar")

    except Exception as e:
        logging.error(f"Error in daily automation: {str(e)}", exc_info=True)
        # Optionally send an error notification (e.g., email, SMS)

if __name__ == "__main__":
    main()
