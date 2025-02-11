import os
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    # Email configuration from environment variables
    sender_email = os.getenv('EMAIL_SENDER')
    sender_password = os.getenv('EMAIL_PASSWORD')
    recipient_email = os.getenv('RECIPIENT_EMAIL')

    if not all([sender_email, sender_password, recipient_email]):
        logging.warning("Email configuration is incomplete. Skipping email.")
        return

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"Football Matches for {datetime.now().strftime('%Y-%m-%d')}"

    # Get matches summary
    matches_summary = format_matches_summary()

    # Email body
    body = f"""
Hello Football Fan,

Here are today's matches:

{matches_summary}

These matches have been added to your calendar automatically.
You can find the calendar file attached to this email.

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
        logging.error(f"Calendar file {calendar_path} not found.")
        return

    # Send the email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        logging.info("Email sent successfully")
    except Exception as e:
        logging.error(f"Error sending email: {e}")

if __name__ == "__main__":
    send_calendar_email()
