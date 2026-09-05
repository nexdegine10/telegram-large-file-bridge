import os
import threading
from flask import Flask, jsonify
from telethon import TelegramClient, events

app = Flask(__name__)

API_ID = int(os.environ["TELEGRAM_API_ID"])
API_HASH = os.environ["TELEGRAM_API_HASH"]
BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

client = TelegramClient(
    "telegram_bridge",
    API_ID,
    API_HASH
)


@client.on(events.NewMessage)
async def handle_message(event):
    try:
        message = event.message

        if message.video:
            size = message.video.size or 0
            print(
                f"VIDEO RECEIVED: {size / (1024 * 1024):.2f} MB",
                flush=True
            )
        elif message.document:
            size = message.document.size or 0
            print(
                f"DOCUMENT RECEIVED: {size / (1024 * 1024):.2f} MB",
                flush=True
            )
        else:
            print("MESSAGE RECEIVED: no video/document", flush=True)

    except Exception as e:
        print(
            f"MESSAGE ERROR: {type(e).__name__}: {e}",
            flush=True
        )


async def start_telegram():
    await client.start(bot_token=BOT_TOKEN)
    print("Telegram bot connected.", flush=True)


def run_telegram():
    try:
        client.loop.run_until_complete(start_telegram())
        client.run_until_disconnected()
    except Exception as e:
        print(
            f"TELEGRAM ERROR: {type(e).__name__}: {e}",
            flush=True
        )


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


threading.Thread(
    target=run_telegram,
    daemon=True
).start()
