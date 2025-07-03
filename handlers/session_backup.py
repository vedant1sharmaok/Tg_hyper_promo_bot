from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
import os
from database import accounts_col
from utils.sessions import string_to_session_file

router = Router()

@router.message(commands=("backup_sessions"))
async def backup_sessions(msg: types.Message):
    user_id = msg.from_user.id
    accounts = await accounts_col.find({"owner_id": user_id}).to_list(5)
    if not accounts:
        return await msg.answer("🔐 You have no linked sessions.")

    for i, acc in enumerate(accounts, 1):
        filename = f"sessions/{user_id}_{i}.session"
        os.makedirs("sessions", exist_ok=True)
        string_to_session_file(acc["session_string"], filename)

        await msg.answer_document(FSInputFile(filename), caption=f"📦 Session {i} backup")
      
