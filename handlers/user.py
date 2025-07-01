from aiogram import Router, types
from app.database import users_col

router = Router()

@router.message(commands="start")
async def start_cmd(msg: types.Message):
    user = await users_col.find_one({"telegram_id": msg.from_user.id})
    if not user:
        await users_col.insert_one({
            "telegram_id": msg.from_user.id,
            "language": "en",
            "is_admin": False,
        })
    await msg.answer("👋 Welcome to TG Hyper Promo Bot!\nUse /help to get started.")

@router.message(commands="help")
async def help_cmd(msg: types.Message):
    await msg.answer("📋 This bot helps you create and manage Telegram marketing campaigns.")

@router.message(commands="language")
async def language_cmd(msg: types.Message):
    await msg.answer("🌐 Language switching will be supported soon. Default: English 🇬🇧")
# user menu
