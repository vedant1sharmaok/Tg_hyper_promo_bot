import asyncio
from datetime import datetime
from fastapi import FastAPI
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config import BOT_TOKEN
from handlers.user import register_user_handlers
from handlers.admin import register_admin_handlers
from handlers import account, campaign, logs, scraper, ai, admin_panel, import_export, session_backup
from api import api_router
from scheduler import daily_report

# === GLOBAL BOT & DISPATCHER ===
bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

# === REGISTER ALL ROUTERS ON GLOBAL DISPATCHER ===
register_user_handlers(dp)
register_admin_handlers(dp)
dp.include_router(account.router)
dp.include_router(campaign.router)
dp.include_router(logs.router)
dp.include_router(scraper.router)
dp.include_router(ai.router)
dp.include_router(admin_panel.router)
dp.include_router(import_export.router)
dp.include_router(session_backup.router)

# === FASTAPI APP ===
app = FastAPI()
app.include_router(api_router, prefix="/api")

@app.get("/health")
def health():
    return {"status": "ok"}

# === BOT COMMANDS SETUP ===
async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="How it works"),
        BotCommand(command="language", description="Choose language"),
    ]
    await bot.set_my_commands(commands)

# === SCHEDULER LOOP ===
async def scheduler_loop():
    IST = datetime.now().astimezone().tzinfo
    while True:
        now = datetime.now(tz=IST)
        if now.hour == 9 and now.minute < 2:  # Around 9:00 AM IST
            await daily_report(bot)
            await asyncio.sleep(120)  # wait to prevent double-run
        await asyncio.sleep(60)

# === POLLING FUNCTION ===
async def start_polling():
    await dp.start_polling(bot)

# === FASTAPI STARTUP HOOK ===
@app.on_event("startup")
async def on_startup():
    # Set bot commands
    await set_bot_commands(bot)

    # Start scheduler loop (runs independently)
    asyncio.create_task(scheduler_loop())

    # Start polling in a separate task
    asyncio.create_task(start_polling())

# === SCRIPT ENTRYPOINT (for local/testing) ===
if __name__ == "__main__":
    # Run FastAPI app and Aiogram polling in separate tasks
    import uvicorn
    from fastapi import FastAPI
    from aiogram import Dispatcher

    async def run():
        # Run FastAPI app
        uvicorn_proc = asyncio.create_subprocess_exec("uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080")
        await asyncio.gather(
            uvicorn_proc,
            start_polling()  # Run Aiogram polling loop
        )

    asyncio.run(run())
        
