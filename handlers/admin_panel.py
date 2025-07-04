from aiogram import Router, types, F
from aiogram.filters import Command
from database import users_col, campaigns_col, accounts_col
from config import ADMINS

router = Router()

def is_admin(user_id):
    return user_id in ADMINS

@router.message(Commands("panel"))
async def panel_main(msg: types.Message):
    if not is_admin(msg.from_user.id):
        return await msg.answer("🚫 You’re not authorized.")

    await msg.answer("🛠️ Admin Panel\nUse /stats to view system stats.")

@router.message(Commands("stats"))
async def panel_stats(msg: types.Message):
    if not is_admin(msg.from_user.id):
        return await msg.answer("🚫 You’re not authorized.")

    user_count = await users_col.count_documents({})
    campaign_count = await campaigns_col.count_documents({})
    account_count = await accounts_col.count_documents({})

    text = (
        "📊 <b>System Statistics</b>\n\n"
        f"👤 Total Users: <code>{user_count}</code>\n"
        f"📣 Campaigns: <code>{campaign_count}</code>\n"
        f"🔐 Accounts Linked: <code>{account_count}</code>\n"
    )
    await msg.answer(text)
  
