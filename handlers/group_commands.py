from pyrogram import Client, filters
from pyrogram.types import Message, ChatMemberUpdated, ChatPermissions, ChatPrivileges
from pyrogram.enums import ChatMemberStatus
from pyrogram.raw import types
import logging
import db

DEFAULT_WELCOME = "👋 Welcome {first_name} to {title}!"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def register_group_commands(app: Client):

    # ==========================================================
    # WELCOME SYSTEM
    # ==========================================================

    @app.on_message(filters.new_chat_members)
    async def send_welcome(client, message: Message):
        await handle_welcome(
            client,
            message.chat.id,
            message.new_chat_members,
            message.chat.title,
        )

    @app.on_chat_member_updated()
    async def member_update(client, cmu: ChatMemberUpdated):
        if not cmu.old_chat_member or not cmu.new_chat_member:
            return

        old_status = cmu.old_chat_member.status
        new_status = cmu.new_chat_member.status

        if old_status in [ChatMemberStatus.LEFT, ChatMemberStatus.RESTRICTED] \
           and new_status == ChatMemberStatus.MEMBER:
            await handle_welcome(
                client,
                cmu.chat.id,
                [cmu.new_chat_member.user],
                cmu.chat.title,
            )

# ==========================================================
# power logic
# ==========================================================
    async def is_power(client, chat_id: int, user_id: int) -> bool:
        member = await client.get_chat_member(chat_id, user_id)
        return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
