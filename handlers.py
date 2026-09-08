import os
import logging
import asyncio
from dotenv import load_dotenv

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import BusinessConnection, Message

load_dotenv()
ADMIN = os.getenv("ADMIN")

logger = logging.getLogger(__name__)

router = Router()

connections: dict[str, int] = {}

@router.message(CommandStart())
async def boot(message: Message):
    await message.answer("<b>Алоха</b>", parse_mode="HTML")

@router.message(Command("info"))
async def info_hub_call(message: Message):
    await message.answer("info hub")

@router.business_connection()
async def business_connection_handler(conn: BusinessConnection):
    if conn.is_enabled:
        connections[conn.id] = conn.user.id
        logger.info(f"New connection: {conn.id} for user {conn.user.full_name} (can_reply={conn.can_reply})")
    else:
        connections.pop(conn.id)
        logger.info(f"Connection disabled: {conn.id}")

@router.business_message(F.text)
async def message_received(message: Message):
    bot = message.bot
    conn_id = message.business_connection_id

    if message.sender_business_bot is not None: return

    owner_id = connections.get(conn_id)
    if not owner_id:
        conn = await bot.get_business_connection(conn_id)
        owner_id = conn.user.id
        connections[conn_id] = owner_id

    if message.from_user.id == owner_id:
        return

    chat_id = message.chat.id
    try:
        await bot.send_chat_action(
            chat_id=chat_id,
            action="typing",
            business_connection_id=conn_id
        )
        await message.answer("В очередь")

    except Exception as e:
        logger.error(f"Error while sending message: {e}")

    try:
        await bot.read_business_message(
            business_connection_id=conn_id,
            chat_id=chat_id,
            message_id=message.message_id
        )
    except Exception as e:
        logger.error(f"Error while reading message: {e}")



