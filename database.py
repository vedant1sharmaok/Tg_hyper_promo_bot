from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI

mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client.tgPromoDB

users_col = db.users
# MongoDB setup
