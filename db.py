import motor.motor_asyncio
from config import MONGO_URI, DB_NAME
import logging

# setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s'
)

try:
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    logging.info("✅ MongoDB connected successfully!")
except Exception as e:
    logging.error(f"❌ Failed to connect to MongoDB: {e}")

# ==========================================================
# 🟢 WELCOME MESSAGE SYSTEM
# ==========================================================

async def set_welcome_message(chat_id, text: str):
    await db.welcome.update_one(
        {"chat_id": chat_id},
        {"$set": {"message": text}},
        upsert=True
    )

async def get_welcome_message(chat_id):
    data = await db.welcome.find_one({"chat_id": chat_id})
    return data.get("message") if data else None

async def set_welcome_status(chat_id, status: bool):
    await db.welcome.update_one(
        {"chat_id": chat_id},
        {"$set": {"enabled": status}},
        upsert=True
    )

async def get_welcome_status(chat_id) -> bool:
    data = await db.welcome.find_one({"chat_id": chat_id})
    if not data:  # default ON
        return True
    return bool(data.get("enabled", True))


# ==========================================================
# 👥 ADMIN & BAN USER SYSTEM
# ==========================================================

# Admin collection
async def add_admin(user_id: int, added_by: int):
    await db.admins.insert_one({
        "user_id": user_id,
        "added_by": added_by,
        "added_date": datetime.now()
    })

async def remove_admin(user_id: int):
    await db.admins.delete_one({"user_id": user_id})

async def is_admin(user_id: int) -> bool:
    admin = await db.admins.find_one({"user_id": user_id})
    return admin is not None

async def get_all_admins():
    cursor = db.admins.find({})
    admins = []
    async for doc in cursor:
        admins.append(doc["user_id"])
    return admins

# Banned users collection
async def add_banned_user(user_id: int, banned_by: int, reason: str = ""):
    await db.banned_users.insert_one({
        "user_id": user_id,
        "banned_by": banned_by,
        "ban_date": datetime.now(),
        "reason": reason
    })

async def remove_banned_user(user_id: int):
    await db.banned_users.delete_one({"user_id": user_id})

async def is_banned(user_id: int) -> bool:
    banned = await db.banned_users.find_one({"user_id": user_id})
    return banned is not None

async def get_all_banned_users():
    cursor = db.banned_users.find({})
    banned_users = []
    async for doc in cursor:
        banned_users.append(doc["user_id"])
    return banned_users