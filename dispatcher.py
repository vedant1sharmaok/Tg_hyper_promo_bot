import asyncio
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH
from database import db

accounts_col = db.accounts
logs_col = db.logs

async def dispatch_campaign(campaign):
    groups = campaign["target_groups"]
    text = campaign["text"]
    media = campaign["media_path"]
    account_ids = campaign["accounts_used"]
    delay_group = campaign["interval_between_groups"]
    delay_msg = campaign["interval_between_messages"]

    # For now, rotate between accounts (one per group)
    account_cursor = accounts_col.find({"_id": {"$in": account_ids}})
    accounts = await account_cursor.to_list(100)

    for i, group in enumerate(groups):
        acc_index = i % len(accounts)
        acc = accounts[acc_index]

        try:
            client = TelegramClient(StringSession(acc["session_string"]), API_ID, API_HASH)
            await client.connect()

            if not await client.is_user_authorized():
                await client.disconnect()
                continue

            if media:
                await client.send_file(group, media, caption=text)
            else:
                await client.send_message(group, text)

            await logs_col.insert_one({
    "campaign": campaign["name"],
    "group": group,
    "account": acc["phone"],
    "account_owner": campaign["owner_id"],  # 👈
    "timestamp": datetime.utcnow(),
    "status": "failed",
    "error": str(e)
})
            
            })

            await client.disconnect()

        except Exception as e:
            await logs_col.insert_one({
    "campaign": campaign["name"],
    "group": group,
    "account": acc["phone"],
    "account_owner": campaign["owner_id"],  # 👈
    "timestamp": datetime.utcnow(),
    "status": "failed",
    "error": str(e)
})
                
            })

        await asyncio.sleep(delay_group)
          
