from aiogram import Router, types, F
from aiogram.filters import Command
from database import users_col
from aiogram.utils.keyboard import InlineKeyboardBuilder
from services.language import get_lang
from database import users_col
router = Router()

@router.message(commands("language"))
async def language_cmd(msg: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🇬🇧 English", callback_data="lang_en")
    kb.button(text="🇮🇳 हिन्दी", callback_data="lang_hi")
    await msg.answer("🌐 Choose your language:", reply_markup=kb.as_markup())

@router.callback_query(F.data.startswith("lang_"))
async def set_lang(call: types.CallbackQuery):
    lang_code = call.data.split("_")[1]
    await users_col.update_one({"telegram_id": call.from_user.id}, {"$set": {"language": lang_code}})
    await call.message.edit_text("✅ Language updated.")

@router.message(commands("start"))
async def start_cmd(msg: types.Message):
    user = await users_col.find_one({"telegram_id": msg.from_user.id})
    if not user:
        await users_col.insert_one({
            "telegram_id": msg.from_user.id,
            "language": "en",
            "is_admin": False,
        })
    await msg.answer("👋 Welcome to TG Hyper Promo Bot!\nUse /help to get started.")

@router.message(commands("help"))
async def help_cmd(msg: types.Message):
    await msg.answer("📋 This bot helps you create and manage Telegram marketing campaigns.")

@router.message(commands("language"))
async def language_cmd(msg: types.Message):
    await msg.answer("🌐 Language switching will be supported soon. Default: English 🇬🇧")
# user menu
