from os import getenv

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from dotenv import load_dotenv
from loguru import logger

from routers.start_router import start_router
from routers.registration import registration
from routers.admin_router import admin_router
from routers.user_router import user_router

import auxiliary.db as db
import auxiliary.messages as messages
from auxiliary.classes import Slot, Apointment
import config

load_dotenv()
BOT_TOKEN = getenv('BOT_TOKEN')
TECH_CHAT = getenv('TECH_CHAT')

dp = Dispatcher()
dp.include_router(start_router)
start_router.include_routers(registration, admin_router, user_router)

async def clear_db():
    """The function deletes old records from the "Slots" and "Apointments" tables from the database.
    It runs hourly."""
    while True:
        logger.info(f'{messages.CLEANING_RUN}')
        slot = Slot()
        apoint = Apointment()
        await slot.clear_old()
        if config.DELETE_OLD_APOINTMENT:
            await apoint.clear_old()
        await asyncio.sleep(3600)

async def notifier(bot: Bot):
    """The function searches for new entries in the "Apointment" and "Slots" tables and notifies
    about them in the technical chat (TECH_CHAT). This does not include new slots created by the admin,
    but only slots created when a user cancels apointment."""
    while True:
        apoint = Apointment()
        items = await apoint.get_new()
        if items:
            for item in items:
                await bot.send_message(TECH_CHAT, f'{item[3]} (@{item[2]}) {messages.RECORDED} {item[0]} {messages.IN} {item[1]}')
            await apoint.unmark_new()

        slot = Slot()
        items = await slot.get_new()
        if items:
            for item in items:
                await bot.send_message(TECH_CHAT, f'{messages.RECORD} {item[0]} {item[1]} {messages.ABORTED}. {messages.SLOT} {messages.RECORDED_ON_DB}')
            await slot.unmark_new()
        await asyncio.sleep(600)


async def main():
    bot = Bot(token=BOT_TOKEN)
    
    commands = [BotCommand(command='start', description='Старт'),
                BotCommand(command='cancel', description='Отмена')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

    logger.info(messages.BOT_LAUNCHED)
    await db.init_db()
    asyncio.create_task(clear_db())
    asyncio.create_task(notifier(bot))
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())