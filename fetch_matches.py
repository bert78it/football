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


# Simula un controllo del calendario
def get_calendar_events():
    # Puoi sostituire questa funzione con una logica reale per recuperare eventi dal calendario.
    # Qui, restituiremo una lista vuota per simulare "nessun evento".
    return []


# Funzione principale per verificare l'ora e inviare il messaggio
def main():
    # Imposta il fuso orario di Roma
    rome_tz = timezone(timedelta(hours=1))
    current_time = datetime.now(rome_tz)

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
        print("Non è l'ora prevista per l'invio.")


if __name__ == "__main__":
    # Configura i log
    logging.basicConfig(level=logging.INFO)

    # Carica le variabili d'ambiente
    load_dotenv()

    # Esegue lo script
    main()
