import os
from dotenv import load_dotenv
import logging
from telegram import Bot
import asyncio

logging.basicConfig(level=logging.INFO)

async def test_telegram():
    load_dotenv()
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = '5819014856'
    
    if not bot_token:
        print("ERROR: TELEGRAM_BOT_TOKEN not found in environment")
        return
    
    try:
        bot = Bot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text="Test message - If you see this, your Telegram bot is working!")
        print("SUCCESS: Successfully sent Telegram test message")
    except Exception as e:
        print(f"ERROR: Telegram test failed: {str(e)}")

async def main():
    # Check environment variables
    required_vars = ['API_FOOTBALL_KEY', 'FOOTBALL_DATA_API_KEY', 'TELEGRAM_BOT_TOKEN', 'RECIPIENT_EMAIL']
    for var in required_vars:
        value = os.getenv(var)
        status = "Found" if value else "Missing"
        print(f"[{'OK' if value else 'MISSING'}] {var}: {status}")
    
    # Test Telegram
    await test_telegram()

if __name__ == "__main__":
    asyncio.run(main())
