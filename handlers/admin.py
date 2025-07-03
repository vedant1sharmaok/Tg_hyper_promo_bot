from aiogram import Router, types
from config import ADMINS

router = Router()

@router.message(commands="admin")
async def admin_panel(msg: types.Message):
    if msg.from_user.id not in ADMINS:
        return await msg.answer("🚫 You are not an admin.")
    await msg.answer("🛠 Admin panel loaded. More tools coming soon.")
  
__all__ = ["router"]
