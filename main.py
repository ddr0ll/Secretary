import asyncio
import os
from dotenv import load_dotenv
import logging
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from handlers import router

load_dotenv()
TOKEN = os.getenv("TOKEN")
PORT = os.getenv("PORT", 10000)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(name)s) %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

bot = Bot(TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def nudge(_: web.Request):
    return web.Response(text='OK', status=200)

async def boot_webserver():
    try:
        app = web.Application()

        app.router.add_get('/', nudge)

        runner = web.AppRunner(app)
        await runner.setup()

        site = web.TCPSite(runner, '0.0.0.0', PORT)
        await site.start()

        logger.info('Webserver started successfully')
        return runner

    except Exception as e:
        logger.error(f'Error while starting webserver: {e}')


async def setup_commands(bot: Bot):
    commands = [
        BotCommand(command="info", description="info hub")
    ]
    await bot.set_my_commands(
        commands,
        scope=BotCommandScopeDefault()
    )

async def main():
    runner = None
    try:
        runner = await boot_webserver()
    except Exception as e:
        logger.error(f'Error while starting webserver: {e}')

    try:
        dp.startup.register(setup_commands)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f'Error while starting Bot polling: {e}')
    finally:
        if runner:
            await runner.cleanup()
            logger.info('Webserver was shut down successfully')

if __name__ == "__main__":
    asyncio.run(main())
