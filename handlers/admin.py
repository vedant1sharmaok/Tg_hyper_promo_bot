from aiogram import Router, types
from aiogram.filters import Command
from config import ADMINS

router = Router()

@router.message(Command("admin"))
async def admin_panel(msg: types.Message):
    if msg.from_user.id not in ADMINS:
        return await msg.answer("🚫 You are not an admin.")
    await msg.answer("🛠 Admin panel loaded. More tools coming soon.")

def register_admin_handlers(dp: Router):
    dp.include_router(router)

__all__ = ["router"]
