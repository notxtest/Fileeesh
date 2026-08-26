import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
LOG_FILE_NAME = "bot.log"
PORT = os.getenv("PORT", "5010")
OWNER_ID = int(os.getenv("OWNER_ID", "0123456789"))

MSG_EFFECT = 5104841245755180586

SHORT_URL = os.getenv("SHORT_URL", "linkshortify.com")
SHORT_API = os.getenv("SHORT_API", "")
SHORT_TUT = "https://t.me/How_to_Download_7x/26"

# Bot Configuration
SESSION = "yato"
TOKEN = os.getenv("BOT_TOKEN", "")
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
WORKERS = 5

DB_URI = os.getenv("DB_URI", "mongodb")
DB_NAME = os.getenv("DB_NAME", "yato")

# Force Subscription Channels
FSUB_CHANNEL_ID = int(os.getenv("FSUB_CHANNEL_ID", "-1004451251761"))
FSUB_REQUEST_ENABLED = os.getenv("FSUB_REQUEST_ENABLED", "True").lower() == "true"
FSUB_TIMER_MINUTES = int(os.getenv("FSUB_TIMER_MINUTES", "10"))
FSUBS = [[FSUB_CHANNEL_ID, FSUB_REQUEST_ENABLED, FSUB_TIMER_MINUTES]]

# Database Channel (Primary)
DB_CHANNEL = os.getenv("DB_CHANNEL", "")  # just channel id as string

# Multiple Database Channels (can be set via bot settings)
# DB_CHANNELS = {
#     "-1002595092736": {"name": "Primary DB", "is_primary": True, "is_active": True},
#     "-1001234567890": {"name": "Secondary DB", "is_primary": False, "is_active": True}
# }

# Auto Delete Timer (seconds)
AUTO_DEL = 300

# Admin IDs (from env)
ADMINS = [int(admin_id) for admin_id in os.getenv("ADMINS", "").split(",") if admin_id.strip()]

# Bot Settings
DISABLE_BTN = True
PROTECT = True

# Messages Configuration
MESSAGES = {
    "START": "<b>›› ʜᴇʏ!!, {first} ~ <blockquote>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴏᴜʀ ʙᴏᴛ. ɪ ᴀᴍ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ꜰɪɴᴅ ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ ꜰɪʟᴇs ᴇᴀsɪʟʏ ᴀɴᴅ ǫᴜɪᴄᴋʟʏ.</blockquote></b>",
    "FSUB": "<b><blockquote>›› ʜᴇʏ ×</blockquote>\n  ʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ, sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs</b>",
    "ABOUT": "<b>›› ᴀʙᴏᴜᴛ ᴛʜɪs ʙᴏᴛ\n\n<blockquote expandable>🤖 ʙᴏᴛ ɴᴀᴍᴇ: CineVinesFileBot\n👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ: 🐦\n🐍 ʟᴀɴɢᴜᴀɢᴇ: <a href='https://docs.python.org/3/'>Pʏᴛʜᴏɴ 3</a>\n📚 ʟɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ ᴠ2</a>\n🗄️ ᴅᴀᴛᴀʙᴀsᴇ: <a href='https://www.mongodb.com/docs/'>Mᴏɴɢᴏ ᴅʙ</a>\n\nᴛʜɪs ʙᴏᴛ ɪs ᴍᴀᴅᴇ ꜰᴏʀ ꜰɪʟᴇ sʜᴀʀɪɴɢ ᴘᴜʀᴘᴏsᴇs ᴏɴʟʏ.</blockquote></b>",
    "REPLY": "<b>For More Join - @CineVines</b>",
    "SHORT_MSG": "<b>📊 ʜᴇʏ {first}, \n\n‼️ ɢᴇᴛ ᴀʟʟ ꜰɪʟᴇꜱ ɪɴ ᴀ ꜱɪɴɢʟᴇ ʟɪɴᴋ ‼️\n\n ⌯ ʏᴏᴜʀ ʟɪɴᴋ ɪꜱ ʀᴇᴀᴅʏ, ᴋɪɴᴅʟʏ ᴄʟɪᴄᴋ ᴏɴ ᴏᴘᴇɴ ʟɪɴᴋ ʙᴜᴛᴛᴏɴ..</b>",
    "START_PHOTO": "https://graph.org/file/b9f294b8549d8803e2bae-1a97a4394146e77a7b.jpg",
    "FSUB_PHOTO": "https://graph.org/file/b87c6c0b6ea4ff36282f6-da2c3e8dcb62211e0a.jpg",
    "SHORT_PIC": "https://graph.org/file/b9f294b8549d8803e2bae-1a97a4394146e77a7b.jpg",
    "SHORT": "https://graph.org/file/b87c6c0b6ea4ff36282f6-da2c3e8dcb62211e0a.jpg"
}

def LOGGER(name: str, client_name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    formatter = logging.Formatter(
        f"[%(asctime)s - %(levelname)s] - {client_name} - %(name)s - %(message)s",
        datefmt='%d-%b-%y %H:%M:%S'
    )
    file_handler = RotatingFileHandler(LOG_FILE_NAME, maxBytes=50_000_000, backupCount=10)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger