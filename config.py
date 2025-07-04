import os
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
ADMINS = list(map(int, os.getenv("ADMINS", "").split(",")))
OPENAI_KEY = os.getenv("OPENAI_KEY") or "your-openai-key"
ADMINS = [123456789, 987654321]  # Replace with real Telegram user IDs
