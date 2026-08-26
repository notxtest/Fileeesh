import logging
from logging.handlers import RotatingFileHandler

# Bot Configuration
LOG_FILE_NAME = "bot.log"
PORT = '5010'
OWNER_ID = 7171541681

MSG_EFFECT = 5046509860389126442

SHORT_URL = "linkshortify.com" # shortner url 
SHORT_API = "" 
SHORT_TUT = "https://t.me/+5qAwb0OP6-02MTdl"

# Bot Configuration
SESSION = "yato"
TOKEN = "8966687209:AAHM3X1grcK1RNREPD9vvU0ebA9uFPLTl7c"
API_ID = "23640310"
API_HASH = "079f8339732e35e032a64ee020e0b90b"
WORKERS = 5

DB_URI = "mongodb+srv://krishnaonly999:Krishdiya07@cluster0.h4rzpxv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "Cluster0"

FSUBS = [[-1004368668083, True, 10]] # Force Subscription Channels [channel_id, request_enabled, timer_in_minutes]
# Database Channel (Primary)
DB_CHANNEL = -1004451251761   # just put channel id dont add ""
# Multiple Database Channels (can be set via bot settings)
# DB_CHANNELS = {
#     "-1002595092736": {"name": "Primary DB", "is_primary": True, "is_active": True},
#     "-1001234567890": {"name": "Secondary DB", "is_primary": False, "is_active": True}
# }
# Auto Delete Timer (seconds)
AUTO_DEL = 300
# Admin IDs
ADMINS = [7171541681, 7171541681]
# Bot Settings
DISABLE_BTN = True
PROTECT = True

# Messages Configuration
MESSAGES = {
    "START": "<b>›› ʜᴇʏ!!, {first} ~ <blockquote>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴏᴜʀ ʙᴏᴛ. ɪ ᴀᴍ ʜᴇʀᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ꜰɪɴᴅ ᴀɴᴅ ɢᴇᴛ ʏᴏᴜʀ ꜰɪʟᴇs ᴇᴀsɪʟʏ ᴀɴᴅ ǫᴜɪᴄᴋʟʏ.</blockquote></b>",
    "FSUB": "<b><blockquote>›› ʜᴇʏ ×</blockquote>\n  ʏᴏᴜʀ ғɪʟᴇ ɪs ʀᴇᴀᴅʏ ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ, sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ғɪʟᴇs</b>",
    "ABOUT": "<b>›› ᴀʙᴏᴜᴛ ᴛʜɪs ʙᴏᴛ\n\n<blockquote expandable>🤖 ʙᴏᴛ ɴᴀᴍᴇ: Fɪʟᴇ Sʜᴀʀɪɴɢ Bᴏᴛ\n👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ: 🐦\n🐍 ʟᴀɴɢᴜᴀɢᴇ: <a href='https://docs.python.org/3/'>Pʏᴛʜᴏɴ 3</a>\n📚 ʟɪʙʀᴀʀʏ: <a href='https://docs.pyrogram.org/'>Pʏʀᴏɢʀᴀᴍ ᴠ2</a>\n🗄️ ᴅᴀᴛᴀʙᴀsᴇ: <a href='https://www.mongodb.com/docs/'>Mᴏɴɢᴏ ᴅʙ</a>\n\nᴛʜɪs ʙᴏᴛ ɪs ᴍᴀᴅᴇ ꜰᴏʀ ꜰɪʟᴇ sʜᴀʀɪɴɢ ᴘᴜʀᴘᴏsᴇs ᴏɴʟʏ.</blockquote></b>",
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