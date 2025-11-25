from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto
)
from config import BOT_USERNAME, SUPPORT_GROUP, UPDATE_CHANNEL, START_IMAGE, OWNER_ID
import db

def register_handlers(app: Client):

# ==========================================================
# Start Message
# ==========================================================
    async def send_start_menu(message, user):
        text = f"""

   ✨ Hello {user}! ✨

👋 I am Nomad 🤖 

Highlights:
─────────────────────────────
- Smart Anti-Spam & Link Shield
- Adaptive Lock System (URLs, Media, Language & more)
- Modular & Scalable Protection
- Sleek UI with Inline Controls

» More New Features coming soon ...
"""

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚒️ Add to Group ⚒️", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
            [
                InlineKeyboardButton("⌂ Support ⌂", url=SUPPORT_GROUP),
                InlineKeyboardButton("⌂ Update ⌂", url=UPDATE_CHANNEL),
            ],
            [
                InlineKeyboardButton("※ ŎŴɳēŔ ※", user_id=OWNER_ID)
            ],
            [InlineKeyboardButton("📚 Help Commands 📚", callback_data="help")]
        ])

        # If /start command, send a new photo
        if message.text:
            await message.reply_photo(START_IMAGE, caption=text, reply_markup=buttons)
        else:
            # If callback, edit the same message
            media = InputMediaPhoto(media=START_IMAGE, caption=text)
            await message.edit_media(media=media, reply_markup=buttons)

# ==========================================================
# Start Command
# ==========================================================
    @app.on_message(filters.private & filters.command("start"))
    async def start_command(client, message):
        user = message.from_user
        await db.add_user(user.id, user.first_name)
        await send_start_menu(message, user.first_name)

# ==========================================================
# Help Menu Message
# ==========================================================
    async def send_help_menu(message):
        text = """
╔══════════════════╗
     Help Menu
╚══════════════════╝

Choose a category below to explore commands:
─────────────────────────────
"""
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⌂ Greetings ⌂", callback_data="greetings"),
                InlineKeyboardButton("⌂ Locks ⌂", callback_data="locks"),
            ],
            [
                InlineKeyboardButton("⌂ Moderation ⌂", callback_data="moderation")
            ],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_start")]
        ])

        media = InputMediaPhoto(media=START_IMAGE, caption=text)
        await message.edit_media(media=media, reply_markup=buttons)

# ==========================================================
# Help Callback_query
# ==========================================================
    @app.on_callback_query(filters.regex("help"))
    async def help_callback(client, callback_query):
        await send_help_menu(callback_query.message)
        await callback_query.answer()

# ==========================================================
# back to start Callback_query
# ==========================================================
    @app.on_callback_query(filters.regex("back_to_start"))
    async def back_to_start_callback(client, callback_query):
        user = callback_query.from_user.first_name
        await send_start_menu(callback_query.message, user)
        await callback_query.answer()