import asyncio
from datetime import datetime, timedelta
from database import logs_col, users_col
from aiogram import Bot
from collections import defaultdict
import pytz

IST = pytz.timezone("Asia/Kolkata")

async def daily_report(bot: Bot):
    print("📨 Running daily campaign reports...")

    start_time = datetime.now(tz=IST) - timedelta(days=1)
    logs = await logs_col.find({"timestamp": {"$gte": start_time}}).to_list(500)

    report_data = defaultdict(lambda: defaultdict(lambda: {"success": 0, "failed": 0}))

    for log in logs:
        uid = log["account_owner"]
        cname = log.get("campaign_name", "Unnamed")
        status = log.get("status")
        if status == "success":
            report_data[uid][cname]["success"] += 1
        else:
            report_data[uid][cname]["failed"] += 1

    for user_id, campaigns in report_data.items():
        lines = ["📊 <b>Your Daily Campaign Report</b>\n"]
        for cname, stats in campaigns.items():
            lines.append(
                f"• <b>{cname}</b> — ✅ {stats['success']} | ❌ {stats['failed']}"
            )
        text = "\n".join(lines)
        try:
            await bot.send_message(user_id, text)
        except:
            continue
      
