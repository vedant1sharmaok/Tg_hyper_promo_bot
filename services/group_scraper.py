from telethon import TelegramClient
from telethon.sessions import StringSession
from config import API_ID, API_HASH

async def search_public_groups(session_str, query, limit=10):
    client = TelegramClient(StringSession(session_str), API_ID, API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        await client.disconnect()
        return []

    results = []
    async for dialog in client.iter_dialogs():
        if dialog.is_group and query.lower() in dialog.name.lower():
            if dialog.entity.username and dialog.entity.participants_count > 30:
                results.append({
                    "name": dialog.name,
                    "username": dialog.entity.username,
                    "members": dialog.entity.participants_count
                })
            if len(results) >= limit:
                break

    await client.disconnect()
    return results
          
