import os
import logging
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
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

# Funzione per eliminare notifiche di Telegram più vecchie di 24 ore
def delete_old_telegram_messages() -> None:
    telegram_bot_token = sanitize_env_var(os.getenv("TELEGRAM_BOT_TOKEN"))
    chat_id = sanitize_env_var(os.getenv("TELEGRAM_CHAT_ID"))
    url = f"https://api.telegram.org/bot{telegram_bot_token}/getUpdates"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            updates = response.json().get("result", [])
            now = datetime.now(timezone.utc)

            for update in updates:
                if "message" in update:
                    message_date = datetime.fromtimestamp(update["message"]["date"], timezone.utc)
                    message_id = update["message"]["message_id"]

                    # Controlla se il messaggio è più vecchio di 24 ore
                    if now - message_date > timedelta(hours=24):
                        delete_url = f"https://api.telegram.org/bot{telegram_bot_token}/deleteMessage"
                        payload = {
                            "chat_id": chat_id,
                            "message_id": message_id
                        }
                        delete_response = requests.post(delete_url, json=payload)
                        if delete_response.status_code == 200:
                            logging.info(f"Deleted message ID {message_id}")
                        else:
                            logging.error(f"Failed to delete message ID {message_id}: {delete_response.text}")
        else:
            logging.error(f"Failed to fetch updates: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error during Telegram API call: {e}")

# Nuova funzione aggiunta per ottenere gli eventi del calendario
def get_calendar_events():
    # Placeholder: inserisci logica reale per ottenere eventi del calendario
    return ["Evento 1 alle 14:00", "Evento 2 alle 18:00"]

# Funzione principale per verificare l'ora e inviare il messaggio
def main():
    # Imposta il fuso orario di Roma
    rome_tz = ZoneInfo("Europe/Rome")
    current_time = datetime.now(rome_tz)

    # Esegue la cancellazione dei messaggi obsoleti
    delete_old_telegram_messages()

    # Controlla se è mezzogiorno
    if current_time.hour == 12 and current_time.minute == 0:
        calendar_events = get_calendar_events()
        if calendar_events:
            # Costruisce un messaggio con gli eventi del calendario
            message = "Ecco il calendario di oggi:\n" + "\n".join(calendar_events)
        else:
            # Messaggio per indicare che non ci sono eventi
            message = "Non ci sono eventi calendarizzati per oggi."
        send_telegram_message(message)
    else:
        logging.info("Non è l'ora prevista per l'invio.")

if __name__ == "__main__":
    # Configura i log
    logging.basicConfig(level=logging.INFO)

    # Carica le variabili d'ambiente
    load_dotenv()

    # Esegue lo script
    main()
