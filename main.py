import asyncio

# Dispatcher instance
dp = Dispatcher(storage=MemoryStorage())

# Routers
dp.include_router(account.router)
dp.include_router(campaign.router)
dp.include_router(logs.router)
dp.include_router(scraper.router)
dp.include_router(ai.router)
dp.include_router(admin_panel.router)
dp.include_router(import_export.router)
dp.include_router(session_backup.router)

# Timezone setup (IST fallback)
IST = datetime.now().astimezone().tzinfo

# Scheduler loop for daily reports
async def scheduler_loop(bot):
    while True:
        now = datetime.now(tz=IST)
        if now.hour == 9 and now.minute < 2:  # Around 9:00 AM IST
            await daily_report(bot)
            await asyncio.sleep(120)  # prevent double-run
        await asyncio.sleep(60)

# FastAPI for API endpoints and health check
app = FastAPI()

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(api_router, prefix="/api")

def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")

# Main startup logic
async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    register_user_handlers(dp)
    register_admin_handlers(dp)
    await set_bot_commands(bot)
    asyncio.create_task(scheduler_loop(bot))
    await dp.start_polling(bot)

# Set bot commands for menu
async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="How it works"),
        BotCommand(command="language", description="Choose language"),
    ]
    await bot.set_my_commands(commands)

# Entry point
if __name__ == "__main__":
    # Start FastAPI health check server in a separate thread
    threading.Thread(target=run_fastapi, daemon=True).start()
    asyncio.run(main())
