from telethon import TelegramClient
from telethon.sessions import StringSession
from app.config import API_ID, API_HASH

async def login_with_otp(phone: str, code_callback, password_callback=None):
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.connect()

    await client.send_code_request(phone)
    code = await code_callback()
    try:
        await client.sign_in(phone, code)
    except Exception as e:
        if "2FA" in str(e) and password_callback:
            password = await password_callback()
            await client.sign_in(password=password)
        else:
            raise e
    session_str = client.session.save()
    user = await client.get_me()
    await client.disconnect()
    return session_str, user

async def test_session(session_str):
    client = TelegramClient(StringSession(session_str), API_ID, API_HASH)
    await client.connect()
    user = await client.get_me()
    await client.disconnect()
    return user
  
