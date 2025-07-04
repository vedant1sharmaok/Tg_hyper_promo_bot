from aiogram import Router, types, F
from aiogram.filters import Command
from database import logs_col
from config import ADMINS

router = Router()

@router.message(commands("my_logs"))
async def my_logs(msg: types.Message):
    user_id = msg.from_user.id
    logs = await logs_col.find({"account_owner": user_id}).to_list(100)

    if not logs:
        return await msg.answer("📭 No logs found for your campaigns.")

    sent = sum(1 for l in logs if l["status"] == "sent")
    failed = sum(1 for l in logs if l["status"] == "failed")
    percent = round((sent / (sent + failed)) * 100, 2) if sent + failed > 0 else 0

    text = (
        f"📊 <b>Campaign Analytics</b>\n\n"
        f"✅ Sent: {sent}\n❌ Failed: {failed}\n"
        f"📈 Success Rate: {percent}%"
    )
    await msg.answer(text)

@router.message(commands("all_logs"))
async def all_logs(msg: types.Message):
    if msg.from_user.id not in ADMINS:
        return await msg.answer("🚫 You're not an admin.")

    logs = await logs_col.find().sort("timestamp", -1).to_list(20)
    if not logs:
        return await msg.answer("📭 No system logs yet.")

    text = "🧾 <b>Latest 20 Log Entries</b>\n\n"
    for l in logs:
        text += (
            f"📤 <b>{l['campaign']}</b>\n"
            f"👥 Group: {l['group']}\n"
            f"📱 Account: {l['account']}\n"
            f"📆 Time: {l['timestamp'].strftime('%Y-%m-%d %H:%M')}\n"
            f"🟢 Status: {l['status']}\n"
        )
        if l['status'] == "failed":
            text += f"⚠️ Error: {l.get('error', 'Unknown')}\n"
        text += "\n"

    await msg.answer(text)
  
