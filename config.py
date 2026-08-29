import os
import logging
import secrets
import time
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
LOG_FILE_NAME = "bot.log"
PORT = '5010'
OWNER_ID = int(os.getenv('OWNER_ID'))

MSG_EFFECT = 5046509860389126442

SHORT_URL = "linkshortify.com"
SHORT_API = "" 
SHORT_TUT = "https://t.me/+5qAwb0OP6-02MTdl"

# Bot Configuration
SESSION = os.getenv('SESSION')
TOKEN = os.getenv('TOKEN')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
WORKERS = 5

DB_URI = os.getenv('DB_URI')
DB_NAME = os.getenv('DB_NAME')

FSUBS = [[-1004451251761, True, 10]]
DB_CHANNEL = -1004368668083

AUTO_DEL = 300
ADMINS = [7171541681, 7171541681]

DISABLE_BTN = True
PROTECT = True

# Short Link Token Storage
short_link_tokens = {}

def generate_short_token(user_id, base64_string):
    """Generate unique token for short link"""
    timestamp = int(time.time())
    token = secrets.token_hex(8)
    short_link_tokens[token] = {
        'user_id': user_id,
        'base64_string': base64_string,
        'timestamp': timestamp
    }
    return f"yu3elk_{base64_string}_{token}_7"

def verify_short_token(user_id, payload):
    """Verify token and check time"""
    try:
        parts = payload.split('_')
        if len(parts) != 3:
            return None, None, 0
        
        base64_string = parts[0]
        token = parts[1]
        
        if token not in short_link_tokens:
            return None, base64_string, 0
        
        token_data = short_link_tokens[token]
        
        if token_data['user_id'] != user_id:
            return None, base64_string, 0
        
        time_diff = time.time() - token_data['timestamp']
        del short_link_tokens[token]
        
        if time_diff < 60:
            return "bypass", base64_string, time_diff
        
        return "valid", base64_string, time_diff
        
    except:
        return None, None, 0

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