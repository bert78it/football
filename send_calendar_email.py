import os
import json
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_gmail_service():
    """Gets Gmail service using the same credentials as calendar"""
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
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
        
        # Save the credentials
        with open('credentials/token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

def format_matches_summary():
    """Create a summary of today's matches for the email body"""
    try:
        with open('matches.json', 'r', encoding='utf-8') as f:
            matches = json.load(f)
        
        if not matches:
            return "No matches scheduled for today."
        
        summary = []
        for match in matches:
            match_time = datetime.strptime(match['date'], '%Y-%m-%dT%H:%M:%S%z')
            local_time = match_time.strftime('%H:%M')
            
            match_info = f"{local_time} - {match['home_team']} vs {match['away_team']}"
            if match.get('venue'):
                match_info += f"\nVenue: {match['venue']}"
            summary.append(match_info)
        
        return "\n\n".join(summary)
    except Exception as e:
        logging.error(f"Error creating matches summary: {e}")
        return "Error retrieving match information."

def send_calendar_email():
    try:
        # Get Gmail service
        service = get_gmail_service()
        
        # Create the email message
        msg = MIMEMultipart()
        msg['to'] = os.environ.get('RECIPIENT_EMAIL', 'your-email@gmail.com')
        msg['subject'] = f"Football Matches for {datetime.now().strftime('%Y-%m-%d')}"

        # Get matches summary
        matches_summary = format_matches_summary()

        # Email body
        body = f"""
Hello Football Fan,

Here are today's matches:

{matches_summary}

These matches have been added to your calendar automatically.

Best regards,
Your Football Matches Bot
        """
        msg.attach(MIMEText(body, 'plain'))

        # Attach the calendar file
        calendar_path = 'football_matches_calendar.ics'
        if os.path.exists(calendar_path):
            with open(calendar_path, 'rb') as file:
                part = MIMEApplication(file.read(), Name=os.path.basename(calendar_path))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(calendar_path)}"'
                msg.attach(part)
        else:
            logging.warning(f"Calendar file {calendar_path} not found.")

        # Encode the message
        raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
        
        # Send the email
        service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()
        
        logging.info("Email sent successfully")
    
    except Exception as e:
        logging.error(f"Error sending email: {e}")

if __name__ == "__main__":
    send_calendar_email()
