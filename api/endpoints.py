from fastapi import APIRouter, Depends
from database import campaigns_col, logs_col
from .auth import get_user_from_token
from datetime import datetime

campaigns_api = APIRouter()

@campaigns_api.get("/")
async def list_campaigns(user_id: int = Depends(get_user_from_token)):
    data = await campaigns_col.find({"owner_id": user_id}).to_list(50)
    for c in data:
        c["_id"] = str(c["_id"])
    return data

@campaigns_api.post("/")
async def create_campaign(payload: dict, user_id: int = Depends(get_user_from_token)):
    payload["owner_id"] = user_id
    payload["status"] = "active"
    payload["created_at"] = datetime.utcnow()
    await campaigns_col.insert_one(payload)
    return {"success": True, "message": "Campaign created"}

@campaigns_api.get("/logs")
async def get_logs(user_id: int = Depends(get_user_from_token)):
    logs = await logs_col.find({"account_owner": user_id}).sort("timestamp", -1).to_list(20)
    for l in logs:
        l["_id"] = str(l["_id"])
    return logs

@campaigns_api.post("/control")
async def control_campaign(payload: dict, user_id: int = Depends(get_user_from_token)):
    name = payload.get("name")
    new_status = payload.get("status")  # active | paused | stopped
    result = await campaigns_col.update_one(
        {"owner_id": user_id, "name": name},
        {"$set": {"status": new_status}}
    )
    return {"success": result.modified_count == 1}
  
