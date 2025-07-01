from app.database import db
from datetime import datetime

campaigns_col = db.campaigns

async def save_campaign(owner_id, name, text, media_path, target_groups, accounts_used, delay_group, delay_msg):
    await campaigns_col.insert_one({
        "owner_id": owner_id,
        "name": name,
        "text": text,
        "media_path": media_path,
        "target_groups": target_groups,
        "accounts_used": accounts_used,
        "interval_between_groups": delay_group,
        "interval_between_messages": delay_msg,
        "status": "active",
        "created_at": datetime.utcnow()
    })

async def get_user_campaigns(user_id):
    return await campaigns_col.find({"owner_id": user_id}).to_list(100)

async def update_campaign_status(user_id, name, new_status):
    await campaigns_col.update_one(
        {"owner_id": user_id, "name": name},
        {"$set": {"status": new_status}}
      )
  
