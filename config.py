import os
from dotenv import load_dotenv

load_dotenv()

# VPS --- FILL COOKIES 🍪 in """ ... """ 

INST_COOKIES = """
# wtite up here insta cookies
"""

YTUB_COOKIES = """
# write here yt cookies
"""

API_ID = os.getenv("API_ID", "")
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
MONGO_DB = os.getenv("MONGO_DB", "")

# 👑 Safe Owner ID parsing
owner_id_env = os.getenv("OWNER_ID", "").strip()
OWNER_ID = [int(x) for x in owner_id_env.split() if x.lstrip('-').isdigit()] if owner_id_env else []

DB_NAME = os.getenv("DB_NAME", "telegram_downloader")
STRING = os.getenv("STRING", None) # optional

# 📢 Safe Channel & Force Subscribe Configuration (Defaults to 0 if not configured)
log_group_env = os.getenv("LOG_GROUP", "").strip()
LOG_GROUP = int(log_group_env) if log_group_env and log_group_env.lstrip('-').isdigit() else 0

force_sub_env = os.getenv("FORCE_SUB", "").strip()
FORCE_SUB = int(force_sub_env) if force_sub_env and force_sub_env.lstrip('-').isdigit() else 0

# 🔐 Session Encryption Keys
MASTER_KEY = os.getenv("MASTER_KEY", "SaveRestrictedMasterKeySecure2025") # fallback secure default
IV_KEY = os.getenv("IV_KEY", "SaveRestrictedIVKey2025") # fallback secure default

# 🌐 Official Branding & Session Identity (Fixes "Team SPY" in Telegram Devices)
BOT_NAME = os.getenv("BOT_NAME", "Content Saver Pro")
DEVICE_MODEL = os.getenv("DEVICE_MODEL", "Content Saver Pro")
APP_VERSION = os.getenv("APP_VERSION", "4.0.0 (Official)")
SYSTEM_VERSION = os.getenv("SYSTEM_VERSION", "Linux / Android")

YT_COOKIES = os.getenv("YT_COOKIES", YTUB_COOKIES)
INSTA_COOKIES = os.getenv("INSTA_COOKIES", INST_COOKIES)
FREEMIUM_LIMIT = int(os.getenv("FREEMIUM_LIMIT", "0"))
PREMIUM_LIMIT = int(os.getenv("PREMIUM_LIMIT", "99999999"))
JOIN_LINK = os.getenv("JOIN_LINK", "").strip()
ADMIN_CONTACT = os.getenv("ADMIN_CONTACT", "").strip()

# ⚡ High-Speed Upload & Transmission Settings
MAX_CONCURRENT_TRANSMISSIONS = int(os.getenv("MAX_CONCURRENT_TRANSMISSIONS", "12")) # 12 parallel chunk streams
CHUNK_WORKERS = int(os.getenv("CHUNK_WORKERS", "32")) # High-throughput worker threads
PARALLEL_MEDIA_SESSIONS = int(os.getenv("PARALLEL_MEDIA_SESSIONS", "4")) # Parallel MTProto media TCP connections




