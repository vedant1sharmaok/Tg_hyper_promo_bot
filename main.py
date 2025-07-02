import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from app.config import BOT_TOKEN
from app.handlers.user import register_user_handlers
from app.handlers.admin import register_admin_handlers
from app.handlers import accounts  # ADD THIS
dp.include_router(accounts.router)
from app.handlers import campaigns  # Add to import list
dp.include_router(campaigns.router)
from app.scheduler.runner import scheduler_loop
from app.handlers import logs
dp.include_router(logs.router)
from app.handlers import scraper
dp.include_router(scraper.router)
from app.handlers import ai
dp.include_router(ai.router)
from app.handlers import admin_panel
dp.include_router(admin_panel.router)
from app.handlers import import_export
dp.include_router(import_export.router)
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.api import api_router
from app.handlers import session_backup
dp.include_router(session_backup.router)
from app.scheduler import daily_report
import asyncio

async def scheduler_loop(bot):
    while True:
        now = datetime.now(tz=IST)
        if now.hour == 9 and now.minute < 2:  # Around 9:00 AM IST
            await daily_report(bot)
            await asyncio.sleep(120)  # wait to prevent double-run
        await asyncio.sleep(60)
        
app = FastAPI()
app.include_router(api_router, prefix="/api")

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    register_user_handlers(dp)
    register_admin_handlers(dp)
    dp.include_router(accounts.router)
    dp.include_router(campaigns.router)

    await set_bot_commands(bot)

    asyncio.create_task(scheduler_loop())  # 🔁 Start scheduler loop

    await dp.start_polling(bot)
    
async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="How it works"),
        BotCommand(command="language", description="Choose language"),
    ]
    await bot.set_my_commands(commands)

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    register_user_handlers(dp)
    register_admin_handlers(dp)

    await set_bot_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
