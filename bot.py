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
    print("Telegram bot connected.")


def run_telegram():
    client.loop.run_until_complete(start_telegram())
    client.run_until_disconnected()


@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "service": "telegram-large-file-bridge"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


threading.Thread(target=run_telegram, daemon=True).start()
