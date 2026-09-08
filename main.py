import asyncio
import os
from dotenv import load_dotenv
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from handlers import router

load_dotenv()
TOKEN = os.getenv("TOKEN")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

bot = Bot(TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def setup_commands(bot: Bot):
    commands = [
        BotCommand(command="info", description="info hub")
    ]
    await bot.set_my_commands(
        commands,
        scope=BotCommandScopeDefault()
    )

async def main():
    dp.startup.register(setup_commands)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
