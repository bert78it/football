import os
import logging
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# Funzione per sanitizzare una variabile d'ambiente
def sanitize_env_var(env_var: str) -> str:
    return (
        "".join(filter(lambda x: x.isprintable() and x != "\n", env_var)).strip()
        if env_var
        else ""
    )

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

# Funzione per recuperare eventi dalle API di FootballData.org
def get_calendar_events():
    api_key = sanitize_env_var(os.getenv("FOOTBALLDATA_API_KEY"))
    headers = {"X-Auth-Token": api_key}
    url = "https://api.football-data.org/v4/matches"

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            matches = response.json().get("matches", [])
            today = datetime.now(ZoneInfo("Europe/Rome")).strftime("%Y-%m-%d")
            # Filtra le partite di oggi
            return [
                f"{match['homeTeam']['name']} vs {match['awayTeam']['name']} - {match['utcDate']}"
                for match in matches if match['utcDate'].startswith(today)
            ]
        else:
            logging.error(f"Errore API FootballData: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        logging.error(f"Errore nella chiamata API: {e}")
        return []

# Funzione principale per verificare l'ora e inviare il messaggio
def main():
    from datetime import datetime
from zoneinfo import ZoneInfo
import logging
    # Imposta il fuso orario di Roma
    rome_tz = ZoneInfo("Europe/Rome")
    current_time = datetime.now(rome_tz)
    logging.info(f"Ora corrente: {current_time.isoformat()}")

    # Controlla se è mezzogiorno
    if current_time.hour == 12 and current_time.minute == 0:
        # Il resto del tuo codice per inviare il messaggio...
    pass
    else:
        logging.info("Non è l'ora prevista per l'invio.")

if __name__ == "__main__":
    # Configura i log
    logging.basicConfig(level=logging.INFO)

    # Carica le variabili d'ambiente
    load_dotenv()

    # Esegue lo script
    main()
