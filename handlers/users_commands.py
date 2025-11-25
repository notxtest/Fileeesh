from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from config import OWNER_ID
import db
import logging

logger = logging.getLogger(__name__)

# ==========================================================
# 🛡️ PERMISSION CHECKERS
# ==========================================================

async def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID

async def is_admin(user_id: int) -> bool:
    # Check if user is in admin list
    admin_data = await db.admins.find_one({"user_id": user_id})
    return admin_data is not None or user_id == OWNER_ID

# ==========================================================
# 👥 ADMIN MANAGEMENT SYSTEM
# ==========================================================

def register_users_commands(app: Client):

    # ==========================================================
    # 🤖 ADMIN_LIST COMMAND
    # ==========================================================
    @app.on_message(filters.private & filters.command("admin_list"))
    async def admin_list_command(client, message: Message):
        if not await is_owner(message.from_user.id):
            return await message.reply_text("❌ Only bot owner can use this command.")

        try:
            cursor = db.admins.find({})
            admins = []
            async for doc in cursor:
                admins.append(f"• User ID: `{doc['user_id']}`")

            if not admins:
                text = "📋 **Admin List:**\n\nNo additional admins found.\nOnly owner exists."
            else:
                text = "📋 **Admin List:**\n\n" + "\n".join(admins)
                text += f"\n\n**Total Admins:** {len(admins)}"

            await message.reply_text(text)

        except Exception as e:
            logger.error(f"Error in admin_list: {e}")
            await message.reply_text("❌ Error fetching admin list.")

    # ==========================================================
    # ➕ ADD_ADMINS COMMAND
    # ==========================================================
    @app.on_message(filters.private & filters.command("add_admins"))
    async def add_admins_command(client, message: Message):
        if not await is_owner(message.from_user.id):
            return await message.reply_text("❌ Only bot owner can use this command.")

        parts = message.text.split()
        if len(parts) < 2:
            return await message.reply_text(
                "⚠️ **Usage:** `/add_admins user_id1 user_id2 ...`\n\n"
                "**Example:** `/add_admins 123456789 987654321`"
            )

        added = []
        failed = []

        for user_id_str in parts[1:]:
            if not user_id_str.isdigit():
                failed.append(f"{user_id_str} (Invalid ID)")
                continue

            user_id = int(user_id_str)
            
            # Don't allow adding owner as admin
            if user_id == OWNER_ID:
                failed.append(f"{user_id} (Owner)")
                continue

            try:
                # Check if user already admin
                existing = await db.admins.find_one({"user_id": user_id})
                if existing:
                    failed.append(f"{user_id} (Already admin)")
                    continue

                # Add to admin collection
                await db.admins.insert_one({
                    "user_id": user_id,
                    "added_by": message.from_user.id,
                    "added_date": message.date
                })
                added.append(str(user_id))

            except Exception as e:
                logger.error(f"Error adding admin {user_id}: {e}")
                failed.append(f"{user_id} (Error)")

        # Prepare response
        text = "👥 **Admin Addition Results:**\n\n"
        
        if added:
            text += f"✅ **Added ({len(added)}):**\n{', '.join(added)}\n\n"
        
        if failed:
            text += f"❌ **Failed ({len(failed)}):**\n{', '.join(failed)}"

        await message.reply_text(text)

    # ==========================================================
    # 🗑️ DEL_ADMINS COMMAND
    # ==========================================================
    @app.on_message(filters.private & filters.command("del_admins"))
    async def del_admins_command(client, message: Message):
        if not await is_owner(message.from_user.id):
            return await message.reply_text("❌ Only bot owner can use this command.")

        parts = message.text.split()
        if len(parts) < 2:
            return await message.reply_text(
                "⚠️ **Usage:** `/del_admins user_id1 user_id2 ...`\n\n"
                "**Example:** `/del_admins 123456789 987654321`"
            )

        deleted = []
        failed = []

        for user_id_str in parts[1:]:
            if not user_id_str.isdigit():
                failed.append(f"{user_id_str} (Invalid ID)")
                continue

            user_id = int(user_id_str)

            try:
                result = await db.admins.delete_one({"user_id": user_id})
                if result.deleted_count > 0:
                    deleted.append(str(user_id))
                else:
                    failed.append(f"{user_id} (Not found)")

            except Exception as e:
                logger.error(f"Error deleting admin {user_id}: {e}")
                failed.append(f"{user_id} (Error)")

        # Prepare response
        text = "👥 **Admin Deletion Results:**\n\n"
        
        if deleted:
            text += f"✅ **Deleted ({len(deleted)}):**\n{', '.join(deleted)}\n\n"
        
        if failed:
            text += f"❌ **Failed ({len(failed)}):**\n{', '.join(failed)}"

        await message.reply_text(text)

    # ==========================================================
    # 🔨 BANUSER_LIST COMMAND
    # ==========================================================
    @app.on_message(filters.private & filters.command("banuser_list"))
    async def banuser_list_command(client, message: Message):
        if not await is_admin(message.from_user.id):
            return await message.reply_text("❌ Only admins can use this command.")

        try:
            cursor = db.banned_users.find({})
            banned_users = []
            async for doc in cursor:
                banned_users.append(f"• User ID: `{doc['user_id']}`")

            if not banned_users:
                text = "🚫 **Banned Users List:**\n\nNo banned users found."
            else:
                text = "🚫 **Banned Users List:**\n\n" + "\n".join(banned_users)
                text += f"\n\n**Total Banned:** {len(banned_users)}"

            await message.reply_text(text)

        except Exception as e:
            logger.error(f"Error in banuser_list: {e}")
            await message.reply_text("❌ Error fetching banned users list.")

    # ==========================================================
    # 🚫 ADD_BANUSER COMMAND
    # ==========================================================
    @app.on_message(filters.private & filters.command("add_banuser"))
    async def add_banuser_command(client, message: Message):
        if not await is_admin(message.from_user.id):
            return await message.reply_text("❌ Only admins can use this command.")

        parts = message.text.split()
        if len(parts) < 2:
            return await message.reply_text(
                "⚠️ **Usage:** `/add_banuser user_id1 user_id2 ...`\n\n"
                "**Example:** `/add_banuser 123456789 987654321`"
            )

        added = []
        failed = []

        for user_id_str in parts[1:]:
            if not user_id_str.isdigit():
                failed.append(f"{user_id_str} (Invalid ID)")
                continue

            user_id = int(user_id_str)

            try:
                # Check if user already banned
                existing = await db.banned_users.find_one({"user_id": user_id})
                if existing:
                    failed.append(f"{user_id} (Already banned)")
                    continue

                # Add to banned users collection
                await db.banned_users.insert_one({
                    "user_id": user_id,
                    "banned_by": message.from_user.id,
                    "ban_date": message.date,
                    "reason": "Manual ban by admin"
                })
                added.append(str(user_id))

            except Exception as e:
                logger.error(f"Error banning user {user_id}: {e}")
                failed.append(f"{user_id} (Error)")

        # Prepare response
        text = "🚫 **User Ban Results:**\n\n"
        
        if added:
            text += f"✅ **Banned ({len(added)}):**\n{', '.join(added)}\n\n"
        
        if failed:
            text += f"❌ **Failed ({len(failed)}):**\n{', '.join(failed)}"

        await message.reply_text(text)

    # ==========================================================
    # ✅ DEL_BANUSER COMMAND
    # ==========================================================
    @app.on_message(filters.private & filters.command("del_banuser"))
    async def del_banuser_command(client, message: Message):
        if not await is_admin(message.from_user.id):
            return await message.reply_text("❌ Only admins can use this command.")

        parts = message.text.split()
        if len(parts) < 2:
            return await message.reply_text(
                "⚠️ **Usage:** `/del_banuser user_id1 user_id2 ...`\n\n"
                "**Example:** `/del_banuser 123456789 987654321`"
            )

        deleted = []
        failed = []

        for user_id_str in parts[1:]:
            if not user_id_str.isdigit():
                failed.append(f"{user_id_str} (Invalid ID)")
                continue

            user_id = int(user_id_str)

            try:
                result = await db.banned_users.delete_one({"user_id": user_id})
                if result.deleted_count > 0:
                    deleted.append(str(user_id))
                else:
                    failed.append(f"{user_id} (Not found)")

            except Exception as e:
                logger.error(f"Error unbanning user {user_id}: {e}")
                failed.append(f"{user_id} (Error)")

        # Prepare response
        text = "✅ **User Unban Results:**\n\n"
        
        if deleted:
            text += f"✅ **Unbanned ({len(deleted)}):**\n{', '.join(deleted)}\n\n"
        
        if failed:
            text += f"❌ **Failed ({len(failed)}):**\n{', '.join(failed)}"

        await message.reply_text(text)

    # ==========================================================
    # 🛡️ BAN CHECKER MIDDLEWARE
    # ==========================================================
    @app.on_message(filters.private & ~filters.service, group=-1)
    async def ban_checker(client, message: Message):
        """Check if user is banned before processing any message"""
        try:
            user_id = message.from_user.id
            
            # Skip if user is admin or owner
            if await is_admin(user_id):
                return
            
            # Check if user is banned
            banned = await db.banned_users.find_one({"user_id": user_id})
            if banned:
                await message.reply_text(
                    "🚫 **You are banned from using this bot!**\n\n"
                    "Contact admin for more information."
                )
                await message.stop_propagation()
                
        except Exception as e:
            logger.error(f"Error in ban checker: {e}")

    print("✅ Users commands registered!")