from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client.tgPromoDB

users_col = db.users
campaigns_col = db.campaigns
accounts_col = db.accounts
logs_col = db.logs
# MongoDB setup
