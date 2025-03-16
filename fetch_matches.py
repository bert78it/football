import os
import logging
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta


# Funzione per sanitizzare una variabile d'ambiente
def sanitize_env_var(env_var: str) -> str:
    return (
        "".join(filter(lambda x: x.isprintable() and x != "\n", env_var)).strip()
        if env_var
        else ""
    )


# Funzione per caricare e sanitizzare le variabili d'ambiente
def load_and_sanitize_env_vars():
    """Carica e sanitizza tutte le variabili d'ambiente richieste."""
    env_vars = {
        "TELEGRAM_BOT_TOKEN": sanitize_env_var(os.getenv("TELEGRAM_BOT_TOKEN")),
        "TELEGRAM_CHAT_ID": sanitize_env_var(os.getenv("TELEGRAM_CHAT_ID")),
        "FOOTBALL_DATA_API_KEY": sanitize_env_var(os.getenv("FOOTBALL_DATA_API_KEY")),
    }
    # Log per debug (assicurati di rimuovere in produzione!)
    for key, value in env_vars.items():
        print(f"Sanitized {key}: {repr(value)}")
    return env_vars


# Funzione per inviare un messaggio via Telegram
def send_telegram_message(message: str) -> None:
    telegram_bot_token = sanitize_env_var(os.getenv("TELEGRAM_BOT_TOKEN"))
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": sanitize_env_var(os.getenv("TELEGRAM_CHAT_ID")),
        "text": message,
    }
    try:
        response = requests.post(url, json=payload)
        logging.info(f"Response Code: {response.status_code}")
        logging.info(f"Response Text: {response.text}")
        if response.status_code != 200:
            logging.error(
                f"Failed to send message: {response.status_code} - {response.text}"
            )
    except requests.exceptions.RequestException as e:
        logging.error(f"Exception during Telegram API call: {e}")


# Carica il file .env
load_dotenv()

# Stampa per verificare le variabili d'ambiente
print("TELEGRAM_BOT_TOKEN:", repr(os.getenv("TELEGRAM_BOT_TOKEN")))
print("TELEGRAM_CHAT_ID:", repr(os.getenv("TELEGRAM_CHAT_ID")))
print("FOOTBALL_DATA_API_KEY:", repr(os.getenv("FOOTBALL_DATA_API_KEY")))

# Esempio di utilizzo
env_vars = load_and_sanitize_env_vars()
telegram_bot_token = env_vars["TELEGRAM_BOT_TOKEN"]
telegram_chat_id = env_vars["TELEGRAM_CHAT_ID"]
football_data_api_key = env_vars["FOOTBALL_DATA_API_KEY"]

# Verifica e gestione delle eccezioni per le variabili mancanti
if not telegram_chat_id:
    raise Exception("Missing required environment variable: TELEGRAM_CHAT_ID")
if not telegram_bot_token:
    raise Exception("Missing required environment variable: TELEGRAM_BOT_TOKEN")
if not football_data_api_key:
    raise Exception("Missing required environment variable: FOOTBALL_DATA_API_KEY")

print("Sanitized TELEGRAM_CHAT_ID:", telegram_chat_id)
print("Sanitized TELEGRAM_BOT_TOKEN:", telegram_bot_token)
print("Sanitized FOOTBALL_DATA_API_KEY:", football_data_api_key)

# Esempio di richiesta all'API di Telegram
telegram_api_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
print(f"URL sanitizzato: {repr(telegram_api_url)}")


params = {
    "chat_id": telegram_chat_id,
    "text": "Il calendario delle partite di oggi è pronto!",
}
response = requests.get(telegram_api_url, params=params)
print(response.json())
