from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from config import API_ID, API_HASH

def string_to_session_file(session_string, file_path):
    client = TelegramClient(file_path, API_ID, API_HASH, session=StringSession(session_string))
    client.session.save()

def session_file_to_string(file_path):
    client = TelegramClient(file_path, API_ID, API_HASH)
    client.connect()
    return client.session.save()
  
