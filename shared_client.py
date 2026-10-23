# ⚡ Initialize crypto and upload acceleration before Pyrogram/Telethon initialize
import utils.crypto_patch
from utils.fast_upload import apply_fast_upload_patch
apply_fast_upload_patch()

from telethon import TelegramClient
from telethon.errors import FloodWaitError
from config import (
    API_ID, API_HASH, BOT_TOKEN, STRING,
    MAX_CONCURRENT_TRANSMISSIONS, CHUNK_WORKERS,
    DEVICE_MODEL, APP_VERSION, SYSTEM_VERSION
)
from pyrogram import Client
from pyrogram.errors import FloodWait
import sys

client = TelegramClient(
    "telethonbot",
    API_ID,
    API_HASH,
    device_model=DEVICE_MODEL,
    app_version=APP_VERSION,
    system_version=SYSTEM_VERSION
)
app = Client(
    "pyrogrambot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    device_model=DEVICE_MODEL,
    app_version=APP_VERSION,
    system_version=SYSTEM_VERSION,
    max_concurrent_transmissions=MAX_CONCURRENT_TRANSMISSIONS,
    workers=CHUNK_WORKERS
)
userbot = Client(
    "4gbbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING,
    device_model=DEVICE_MODEL,
    app_version=APP_VERSION,
    system_version=SYSTEM_VERSION,
    max_concurrent_transmissions=MAX_CONCURRENT_TRANSMISSIONS,
    workers=CHUNK_WORKERS
)

async def start_client():
    if not client.is_connected():
        try:
            await client.start(bot_token=BOT_TOKEN)
            print("Telethon bot client started...")
        except FloodWaitError as e:
            print(f"⚠️ Telegram Rate Limit on Bot Token: Wait of {e.seconds}s required on this BOT_TOKEN.")
            print("💡 TIP: Change BOT_TOKEN from @BotFather in Render Environment Variables to start immediately without waiting!")
            raise e
    if STRING:
        try:
            await userbot.start()
            print("Userbot engine started...")
        except Exception as e:
            print(f"⚠️ Premium STRING session is invalid or expired: {e}")
            sys.exit(1)
    await app.start()
    print("Main bot application started...")
    return client, app, userbot

