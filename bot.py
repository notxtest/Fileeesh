import os
import re
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from pyrogram import Client, filters
from pyrogram.types import (
    Message, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    CallbackQuery
)
from pyrogram.enums import ParseMode, ChatMemberStatus
from pymongo import MongoClient
import motor.motor_asyncio

# Load environment variables
load_dotenv()

# Bot Configuration
API_ID = 23640310  # Replace with your API ID
API_HASH = "079f8339732e35e032a64ee020e0b90b"  # Replace with your API Hash
BOT_TOKEN = "8358099035:AAGIQk5Y7DYSgMT0hKO5_ssivqRv2DA_9gs"
MONGO_URL = "mongodb+srv://useformyacc:Useformyacc@cluster0.umidw0p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
ADMIN_IDS = [8190398973, 7171541681]
BOT_USERNAME = "Anime_Providing_Bot"
WELCOME_PIC_URL = "https://files.catbox.moe/g0h5if.mp4"
WELCOME_MESSAGE = "👋 Welcome {first_name}!\n\nSearch any anime by typing its name!"
LOG_CHANNEL = -1003153488491

# MongoDB Setup
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client.anime_bot
users_collection = db.users
files_collection = db.files
fsub_collection = db.fsub
settings_collection = db.settings
database_channels_collection = db.database_channels
logs_collection = db.user_logs

# Store user sessions
user_sessions = {}

# Initialize Pyrogram Client
app = Client(
    "anime_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Clean anime name function
def clean_anime_name(dirty_name):
    remove_words = ['hindi dub', 'dubbed', 'subbed', 'english', 'by @', 'by', '@']
    clean_name = dirty_name.lower()
    
    for word in remove_words:
        clean_name = clean_name.replace(word, '')
    
    clean_name = re.sub(r'[^\w\s]', ' ', clean_name)
    clean_name = re.sub(r'\s+', ' ', clean_name)
    clean_name = clean_name.strip().title()
    
    return clean_name

# Parse filename function  
def parse_filename(filename):
    quality_match = re.search(r'\[?(\d+p)\]?', filename, re.IGNORECASE)
    quality = quality_match.group(1) if quality_match else None
    
    episode_match = re.search(r'\[E-(\d+)\]|Episode\s*(\d+)|Ep\s*(\d+)|\[Ep\s*(\d+)\]', filename, re.IGNORECASE)
    episode = None
    if episode_match:
        for group in episode_match.groups():
            if group and group.isdigit():
                episode = int(group)
                break
    
    season_match = re.search(r'\[S-(\d+)\]|S(\d+)E|Season\s*(\d+)|\[Season\s*(\d+)\]', filename, re.IGNORECASE)
    season = None
    if season_match:
        for group in season_match.groups():
            if group and group.isdigit():
                season = int(group)
                break
    
    temp_name = filename
    if quality:
        temp_name = temp_name.replace(f'[{quality}]', '').replace(quality, '')
    if episode:
        temp_name = re.sub(r'\[E-(\d+)\]|Episode\s*\d+|Ep\s*\d+', '', temp_name, flags=re.IGNORECASE)
    if season:
        temp_name = re.sub(r'\[S-(\d+)\]|S\d+E|Season\s*\d+', '', temp_name, flags=re.IGNORECASE)
    
    anime_name = re.sub(r'[^\w\s]', ' ', temp_name)
    anime_name = re.sub(r'\s+', ' ', anime_name)
    anime_name = clean_anime_name(anime_name)
    
    return {
        'anime_name': anime_name,
        'season': season,
        'episode': episode,
        'quality': quality,
        'original_name': filename
    }

# Send logs to private channel
async def send_log_to_channel(log_data: dict):
    try:
        user = log_data.get('user', {})
        activity = log_data.get('activity', {})
        
        log_message = f"""
📊 **USER ACTIVITY LOG**

👤 **User Info:**
├─ Name: {user.get('first_name', 'N/A')}
├─ Username: @{user.get('username', 'N/A')}
├─ ID: `{user.get('user_id', 'N/A')}`
└─ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📝 **Activity Type:** {activity.get('type', 'N/A')}

🔍 **Search Details:**
├─ Query: {activity.get('search_query', 'N/A')}
├─ Anime: {activity.get('anime_name', 'N/A')}
├─ Season: {activity.get('season', 'N/A')}
├─ Episode: {activity.get('episode', 'N/A')}
└─ Quality: {activity.get('quality', 'N/A')}

📁 **File Details:**
├─ Files Sent: {activity.get('files_sent', 0)}
├─ File Names: {activity.get('file_names', [])}
└─ Status: {activity.get('status', 'N/A')}
"""
        await app.send_message(
            chat_id=LOG_CHANNEL,
            text=log_message,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        print(f"Log sending error: {e}")

# Log user activity
async def log_activity(user_id: int, activity_type: str, details: dict):
    try:
        user = await users_collection.find_one({'user_id': user_id})
        if not user:
            user = {
                'user_id': user_id,
                'first_name': 'Unknown',
                'username': 'Unknown'
            }
        
        log_data = {
            'user_id': user_id,
            'activity_type': activity_type,
            'details': details,
            'timestamp': datetime.now(),
            'user': {
                'user_id': user_id,
                'first_name': user.get('first_name', 'Unknown'),
                'username': user.get('username', 'Unknown')
            },
            'activity': {
                'type': activity_type,
                **details
            }
        }
        
        # Save to database
        await logs_collection.insert_one(log_data)
        
        # Send to log channel
        await send_log_to_channel(log_data)
        
    except Exception as e:
        print(f"Logging error: {e}")

# Check if user joined FSub channels
async def check_fsub(user_id: int):
    try:
        fsub_channels = await fsub_collection.find({}).to_list(length=5)
        
        for channel in fsub_channels:
            try:
                member = await app.get_chat_member(channel['chat_id'], user_id)
                if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
                    return False, channel
            except Exception as e:
                print(f"FSub check error: {e}")
                return False, channel
        
        return True, None
    except Exception as e:
        print(f"FSub error: {e}")
        return True, None

# Start command handler
@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    
    # Add user to database
    await users_collection.update_one(
        {'user_id': user_id},
        {'$set': {
            'first_name': first_name,
            'username': message.from_user.username,
            'last_active': datetime.now(),
            'joined_date': datetime.now()
        }},
        upsert=True
    )
    
    # Log start activity
    await log_activity(user_id, 'start', {
        'search_query': '/start',
        'status': 'user_started_bot'
    })
    
    # Check FSub
    joined, channel = await check_fsub(user_id)
    if not joined:
        keyboard = [
            [InlineKeyboardButton(channel['button_name'], url=f"https://t.me/{channel['chat_title']}")],
            [InlineKeyboardButton("Try Again", callback_data="fsub_check")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await message.reply_text(
            f"❌ Join required!\n\nPlease join our channel to access files:",
            reply_markup=reply_markup
        )
        return
    
    # Send welcome message with photo
    welcome_text = WELCOME_MESSAGE.format(first_name=first_name)
    
    try:
        await message.reply_photo(
            photo=WELCOME_PIC_URL,
            caption=welcome_text
        )
    except:
        await message.reply_text(welcome_text)

# Handle text messages (anime search) - FIXED LINE
@app.on_message(filters.text & filters.private)
async def handle_message(client, message: Message):
    user_id = message.from_user.id
    user_input = message.text
    
    # Log search activity
    await log_activity(user_id, 'search', {
        'search_query': user_input,
        'status': 'search_initiated'
    })
    
    # Check FSub first
    joined, channel = await check_fsub(user_id)
    if not joined:
        keyboard = [
            [InlineKeyboardButton(channel['button_name'], url=f"https://t.me/{channel['chat_title']}")],
            [InlineKeyboardButton("Try Again", callback_data="fsub_check")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await message.reply_text(
            f"❌ Join required!\n\nPlease join our channel to access files:",
            reply_markup=reply_markup
        )
        return
    
    # Search for anime in database
    search_query = clean_anime_name(user_input)
    
    # Get all database channels
    db_channels = await database_channels_collection.find({}).to_list(length=2)
    
    all_files = []
    for channel in db_channels:
        # Here you would fetch files from the database channel
        # For now, we'll search in files_collection
        files = await files_collection.find({
            'anime_name': {'$regex': search_query, '$options': 'i'}
        }).to_list(length=100)
        all_files.extend(files)
    
    if not all_files:
        await log_activity(user_id, 'search', {
            'search_query': user_input,
            'anime_name': search_query,
            'status': 'no_files_found'
        })
        await message.reply_text("❌ No files found for your search.")
        return
    
    # Determine content type and show appropriate buttons
    has_seasons = any(file.get('season') for file in all_files)
    has_episodes = any(file.get('episode') for file in all_files)
    
    if has_seasons:
        # Show season selection
        seasons = list(set([file['season'] for file in all_files if file.get('season')]))
        seasons.sort()
        
        keyboard = []
        row = []
        for i, season in enumerate(seasons):
            row.append(InlineKeyboardButton(f"S{season}", callback_data=f"season_{season}"))
            if len(row) == 5 or i == len(seasons) - 1:
                keyboard.append(row)
                row = []
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text(
            f"Anime: {search_query}\n\nSelect season:",
            reply_markup=reply_markup
        )
        
        # Store session
        user_sessions[user_id] = {
            'anime_name': search_query,
            'search_query': user_input,
            'files': all_files,
            'step': 'season_selection'
        }
    
    elif has_episodes:
        # Show episode range selection
        episodes = [file['episode'] for file in all_files if file.get('episode')]
        total_episodes = max(episodes) if episodes else 0
        
        keyboard = []
        ranges = [(i, min(i+49, total_episodes)) for i in range(1, total_episodes, 50)]
        
        row = []
        for i, (start, end) in enumerate(ranges):
            row.append(InlineKeyboardButton(f"{start}-{end}", callback_data=f"eprange_{start}_{end}"))
            if len(row) == 3 or i == len(ranges) - 1:
                keyboard.append(row)
                row = []
        
        keyboard.append([InlineKeyboardButton("Custom Range", callback_data="custom_range")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await message.reply_text(
            f"Anime: {search_query}\nTotal Episodes: {total_episodes}\n\nSelect episode range:",
            reply_markup=reply_markup
        )
        
        # Store session
        user_sessions[user_id] = {
            'anime_name': search_query,
            'search_query': user_input,
            'files': all_files,
            'total_episodes': total_episodes,
            'step': 'episode_selection'
        }
    
    else:
        # Movies - direct quality selection
        qualities = list(set([file['quality'] for file in all_files if file.get('quality')]))
        qualities.sort(key=lambda x: int(x.replace('p', '')) if x else 0)
        
        keyboard = []
        row = []
        for i, quality in enumerate(qualities):
            row.append(InlineKeyboardButton(quality, callback_data=f"quality_{quality}"))
            if len(row) == 2 or i == len(qualities) - 1:
                keyboard.append(row)
                row = []
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text(
            f"Movie: {search_query}\n\nSelect quality:",
            reply_markup=reply_markup
        )
        
        # Store session
        user_sessions[user_id] = {
            'anime_name': search_query,
            'search_query': user_input,
            'files': all_files,
            'step': 'quality_selection'
        }

# Callback query handler
@app.on_callback_query()
async def handle_callback(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    data = callback_query.data
    
    # Handle FSub check
    if data == "fsub_check":
        joined, channel = await check_fsub(user_id)
        if not joined:
            await callback_query.edit_message_text(
                "⚠️ You didn't join channel yet!\nPlease join first then click Try Again"
            )
            return
        else:
            await callback_query.edit_message_text("✅ Now you can search for anime!")
            return
    
    # Handle season selection
    elif data.startswith("season_"):
        season = int(data.split("_")[1])
        session = user_sessions.get(user_id, {})
        
        # Log season selection
        await log_activity(user_id, 'season_select', {
            'search_query': session.get('search_query', ''),
            'anime_name': session.get('anime_name', ''),
            'season': season,
            'status': 'season_selected'
        })
        
        # Show quality selection for this season
        files = session.get('files', [])
        season_files = [f for f in files if f.get('season') == season]
        qualities = list(set([f['quality'] for f in season_files if f.get('quality')]))
        qualities.sort(key=lambda x: int(x.replace('p', '')) if x else 0)
        
        keyboard = []
        row = []
        for i, quality in enumerate(qualities):
            row.append(InlineKeyboardButton(quality, callback_data=f"quality_{quality}"))
            if len(row) == 2 or i == len(qualities) - 1:
                keyboard.append(row)
                row = []
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await callback_query.edit_message_text(
            f"Anime: {session.get('anime_name', '')}\nSeason: {season}\n\nSelect quality:",
            reply_markup=reply_markup
        )
        
        # Update session
        user_sessions[user_id].update({
            'selected_season': season,
            'step': 'quality_selection'
        })
    
    # Handle quality selection
    elif data.startswith("quality_"):
        quality = data.split("_")[1]
        session = user_sessions.get(user_id, {})
        
        # Log quality selection
        await log_activity(user_id, 'quality_select', {
            'search_query': session.get('search_query', ''),
            'anime_name': session.get('anime_name', ''),
            'season': session.get('selected_season'),
            'quality': quality,
            'status': 'quality_selected'
        })
        
        # Show confirmation
        keyboard = [
            [InlineKeyboardButton("✅ Yes Definitely", callback_data="confirm_yes")],
            [InlineKeyboardButton("❌ No No", callback_data="confirm_no")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        anime_info = f"Anime: {session.get('anime_name', '')}"
        if session.get('selected_season'):
            anime_info += f"\nSeason: {session.get('selected_season')}"
        anime_info += f"\nQuality: {quality}"
        
        await callback_query.edit_message_text(
            f"{anime_info}\n\nConfirm download?",
            reply_markup=reply_markup
        )
        
        # Update session
        user_sessions[user_id].update({
            'selected_quality': quality,
            'step': 'confirmation'
        })
    
    # Handle confirmation
    elif data == "confirm_yes":
        session = user_sessions.get(user_id, {})
        anime_name = session.get('anime_name', '')
        season = session.get('selected_season')
        quality = session.get('selected_quality', '')
        
        # Get filtered files
        files = session.get('files', [])
        filtered_files = []
        
        if season:
            filtered_files = [f for f in files if f.get('season') == season and f.get('quality') == quality]
        else:
            filtered_files = [f for f in files if f.get('quality') == quality]
        
        # Send files to user
        files_sent = 0
        file_names = []
        
        for file_data in filtered_files[:10]:  # Limit to 10 files
            try:
                # Here you would send the actual file from database channel
                # For now, we'll just send file info
                await app.send_message(
                    chat_id=user_id,
                    text=f"📁 {file_data.get('original_name', 'File')}"
                )
                files_sent += 1
                file_names.append(file_data.get('original_name', ''))
            except Exception as e:
                print(f"File send error: {e}")
        
        # Log file delivery
        await log_activity(user_id, 'file_delivery', {
            'search_query': session.get('search_query', ''),
            'anime_name': anime_name,
            'season': season,
            'quality': quality,
            'files_sent': files_sent,
            'file_names': file_names,
            'status': 'files_delivered'
        })
        
        # Send completion message
        keyboard = [[InlineKeyboardButton("📥 Get Files", callback_data="get_files")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await callback_query.edit_message_text(
            f"✅ {files_sent} files sent to your DM!\n\nClick below to get files:",
            reply_markup=reply_markup
        )
    
    elif data == "confirm_no":
        await callback_query.edit_message_text("❌ Selection cancelled. Start over by typing the anime name.")

# Admin commands
@app.on_message(filters.command("afsub") & filters.private & filters.user(ADMIN_IDS))
async def afsub_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /afsub <chat_id>")
        return
    
    chat_id = message.command[1]
    
    # Ask for button name
    await message.reply_text("Give me button name:")
    user_sessions[message.from_user.id] = {
        'awaiting_button_name': True,
        'fsub_chat_id': chat_id
    }

@app.on_message(filters.command("dfsub") & filters.private & filters.user(ADMIN_IDS))
async def dfsub_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /dfsub <chat_id>")
        return
    
    chat_id = message.command[1]
    await fsub_collection.delete_one({'chat_id': chat_id})
    await message.reply_text("✅ FSub channel removed!")

@app.on_message(filters.command("fsub") & filters.private & filters.user(ADMIN_IDS))
async def fsub_command(client, message: Message):
    fsub_channels = await fsub_collection.find({}).to_list(length=5)
    
    if not fsub_channels:
        await message.reply_text("No FSub channels set.")
        return
    
    message_text = "📋 FSub Channels:\n\n"
    for channel in fsub_channels:
        message_text += f"Chat ID: {channel['chat_id']}\nButton: {channel['button_name']}\n\n"
    
    await message.reply_text(message_text)

# Database channel commands
@app.on_message(filters.command("adb") & filters.private & filters.user(ADMIN_IDS))
async def adb_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /adb <chat_id>")
        return
    
    chat_id = message.command[1]
    
    # Check if we can add more (max 2)
    current_channels = await database_channels_collection.count_documents({})
    if current_channels >= 2:
        await message.reply_text("❌ Maximum 2 database channels allowed!")
        return
    
    await database_channels_collection.insert_one({
        'chat_id': chat_id,
        'added_date': datetime.now(),
        'added_by': message.from_user.id
    })
    
    await message.reply_text("✅ Database channel added!")

@app.on_message(filters.command("ddb") & filters.private & filters.user(ADMIN_IDS))
async def ddb_command(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Usage: /ddb <chat_id>")
        return
    
    chat_id = message.command[1]
    await database_channels_collection.delete_one({'chat_id': chat_id})
    await message.reply_text("✅ Database channel removed!")

@app.on_message(filters.command("db") & filters.private & filters.user(ADMIN_IDS))
async def db_command(client, message: Message):
    db_channels = await database_channels_collection.find({}).to_list(length=2)
    
    if not db_channels:
        await message.reply_text("No database channels set.")
        return
    
    message_text = "📋 Database Channels:\n\n"
    for channel in db_channels:
        message_text += f"Chat ID: {channel['chat_id']}\nAdded: {channel['added_date'].strftime('%Y-%m-%d')}\n\n"
    
    await message.reply_text(message_text)

# Stats command
@app.on_message(filters.command("stats") & filters.private & filters.user(ADMIN_IDS))
async def stats_command(client, message: Message):
    total_users = await users_collection.count_documents({})
    total_files = await files_collection.count_documents({})
    total_logs = await logs_collection.count_documents({})
    
    stats_text = f"""
📊 Bot Statistics:

👥 Total Users: {total_users}
📁 Total Files: {total_files}
📝 Total Logs: {total_logs}
⏰ Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """
    
    await message.reply_text(stats_text)

# Handle button name input
@app.on_message(filters.text & filters.private & filters.user(ADMIN_IDS))
async def handle_button_name(client, message: Message):
    user_id = message.from_user.id
    session = user_sessions.get(user_id, {})
    
    if session.get('awaiting_button_name'):
        button_name = message.text
        chat_id = session.get('fsub_chat_id')
        
        # Get chat title
        try:
            chat = await app.get_chat(chat_id)
            chat_title = chat.title
        except:
            chat_title = "Unknown"
        
        # Add to FSub collection
        await fsub_collection.insert_one({
            'chat_id': chat_id,
            'button_name': button_name,
            'chat_title': chat_title,
            'added_date': datetime.now(),
            'added_by': user_id
        })
        
        await message.reply_text("✅ Successfully added FSub channel!")
        
        # Clean up
        if user_id in user_sessions:
            del user_sessions[user_id]

# Main function
if __name__ == "__main__":
    print("Bot is running...")
    app.run()