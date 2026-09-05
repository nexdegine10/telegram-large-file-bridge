import os
import threading
from flask import Flask, jsonify
from telethon import TelegramClient

app = Flask(__name__)

API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

client = TelegramClient(
    "telegram_bridge",
    API_ID,
    API_HASH
)


async def start_telegram():
    await client.start(bot_token=BOT_TOKEN)
    print("Telegram bot connected.", flush=True)


def run_telegram():
    try:
        client.loop.run_until_complete(start_telegram())
        client.run_until_disconnected()
    except Exception as e:
        print(f"TELEGRAM ERROR: {type(e).__name__}: {e}", flush=True)


@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "service": "telegram-large-file-bridge"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


threading.Thread(target=run_telegram, daemon=True).start()
