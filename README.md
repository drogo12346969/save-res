# Content Saver & Forwarder Bot

An enterprise-grade Telegram Content Saver, Cloner, and Media Downloader bot built on Python, Pyrogram V2, and Telethon. Designed for high-throughput batch extraction, topic-enabled forum cloning, YouTube/Instagram downloading, and encrypted multi-session management.

---

## ⚡ Core Features

- **Channel & Forum Extraction:** Retrieve media, messages, and topics from public and private Telegram channels/groups.
- **Custom Device Branding:** Logged-in user sessions register under your official branded device name in Telegram's active sessions (`Settings > Devices`).
- **End-to-End Session Encryption:** Session strings stored in MongoDB are encrypted using AES (CBC mode) with PBKDF2 key derivation.
- **Topic-Aware Forum Forwarding:** Direct uploads to specific forum topics (`message_thread_id`) in supergroups.
- **Custom Bot Delegation (`/setbot`):** Delegate extraction workloads to user-provided sub-bots to eliminate rate limits on the primary bot.
- **Direct Media Downloader:** Download videos and audio from YouTube, Instagram, and 30+ supported services via `yt-dlp`.
- **4GB File Uploads:** Supports large file transfers using Telegram Premium user sessions.
- **Built-in Web Server:** Includes a lightweight web service with health checks (`/health`), security headers, Terms of Service, and Privacy Policy.

---

## 📋 Commands

| Command | Description |
| :--- | :--- |
| `/start` | Start the bot and view account status |
| `/batch` | Extract a batch range of messages from a channel/group |
| `/login` | Securely log in using Telegram phone OTP |
| `/logout` | Terminate active user session from the bot |
| `/session` | Connect an existing Pyrogram V2 session string |
| `/setbot` | Connect a dedicated bot token for faster downloads |
| `/rembot` | Remove your custom bot token |
| `/settings` | Customize caption, thumbnail, topic ID, and word replacements |
| `/dl [link]` | Download video from external platforms (YouTube, Instagram, etc.) |
| `/adl [link]` | Download audio from supported platforms |
| `/cancel` | Stop an ongoing batch extraction process |
| `/status` | View plan details and batch expiration time |
| `/plan` | View premium subscription options |
| `/stats` | View bot performance and user metrics (Admin only) |
| `/add [id]` | Upgrade a user to Premium (Admin only) |
| `/rem [id]` | Revoke a user's Premium access (Admin only) |

---

## ⚙️ Configuration (`.env`)

Create a `.env` file in the root directory:

```env
# Telegram Core Credentials (from https://my.telegram.org)
API_ID=12345678
API_HASH=abcdef0123456789abcdef0123456789
BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Branding & Device Info
BOT_NAME="Content Saver"
DEVICE_MODEL="ContentSaver Session"
APP_VERSION="3.0.0"
SYSTEM_VERSION="Linux 6.x"

# Database & Administration
MONGO_DB=mongodb+srv://<username>:<password>@cluster.mongodb.net/
DB_NAME=telegram_downloader
OWNER_ID=123456789

# Channel Enforcement & Logs (Set 0 to disable)
FORCE_SUB=0
LOG_GROUP=0

# Security (AES Encryption Keys)
MASTER_KEY=gK8HzLfT9QpViJcYeB5wRa3DmN7P2xUq
IV_KEY=s7Yx5CpVmE3F4012

# Optional Support Links
ADMIN_CONTACT=https://t.me/YourSupport
JOIN_LINK=https://t.me/YourChannel
```

---

## 🚀 Deployment

### Standard VPS / Local Environment

1. **Clone the repository:**
   ```bash
   git clone <repo_url>
   cd save-res-main
   ```

2. **Install system dependencies:**
   ```bash
   sudo apt update
   sudo apt install -y python3 python3-pip ffmpeg git
   ```

3. **Install Python packages:**
   ```bash
   pip3 install -r requirements.txt
   ```

4. **Launch the application:**
   ```bash
   python3 main.py
   ```

---

## 🔒 Security & Privacy

- All user authentication strings are encrypted at rest using AES-CBC before being written to MongoDB.
- Device sessions registered via the bot carry official device headers, preventing unverified or misleading device identification in Telegram.
- The built-in web portal enforces standard HTTP security headers (CSP, HSTS, X-Content-Type-Options, Frame Options).
