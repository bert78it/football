
import os
import requests

# Stampa i valori delle variabili di ambiente
print("TELEGRAM_CHAT_ID:", os.getenv('TELEGRAM_CHAT_ID'))
print("TELEGRAM_BOT_TOKEN:", os.getenv('TELEGRAM_BOT_TOKEN'))
print("FOOTBALL_DATA_API_KEY:", os.getenv('FOOTBALL_DATA_API_KEY'))

# Codice esistente...
import os
from dotenv import load_dotenv
import asyncio
from telegram import Bot
import logging

logging.basicConfig(level=logging.INFO)

async def send_test_match_notification():
    load_dotenv()
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = '5819014856'
    
    test_match = {
        'home_team': 'Real Madrid',
        'away_team': 'Barcelona',
        'competition': 'La Liga',
        'date': '2025-03-09T23:00:00+01:00'
    }
    
    message = f"""
⚡ *Upcoming Match Alert!*
🇪🇸 *{test_match['home_team']} vs {test_match['away_team']}*

⏰ Starts in: 30 minutes
🏆 Competition: {test_match['competition']}
📅 Date: {test_match['date']}

_Get ready for kickoff!_ 🎮
    """
    
    try:
        bot = Bot(token=bot_token)
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode='Markdown'
        )
        print("✅ Test match notification sent successfully!")
    except Exception as e:
        print(f"❌ Error sending notification: {str(e)}")

if __name__ == "__main__":
    asyncio.run(send_test_match_notification())
