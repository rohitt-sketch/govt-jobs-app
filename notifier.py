# notifier.py
import requests
import streamlit as st

def send_telegram(message):
    # Streamlit ki secrets se token aur ID uthao
    TELEGRAM_BOT_TOKEN = st.secrets["TELEGRAM_BOT_TOKEN"]
    TELEGRAM_CHAT_ID = st.secrets["TELEGRAM_CHAT_ID"]
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        r = requests.post(url, data=payload, timeout=15)
        if r.status_code == 200:
            print("✅ Telegram message chala gaya!")
        else:
            print(f"❌ Error: {r.text}")
    except Exception as e:
        print(f"❌ Error: {e}")