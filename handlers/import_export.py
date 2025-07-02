from aiogram import Router, types
from aiogram.types import FSInputFile
from app.database import campaigns_col
import json
import os

router = Router()

@router.message(commands="export_campaigns")
async def export_user_campaigns(msg: types.Message):
    user_id = msg.from_user.id
    campaigns = await campaigns_col.find({"owner_id": user_id}).to_list(100)
    if not campaigns:
        return await msg.answer("📭 You have no campaigns to export.")

    export_data = [{k: v for k, v in c.items() if k != "_id"} for c in campaigns]

    filename = f"campaign_export_{user_id}.json"
    filepath = f"static/exports/{filename}"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, default=str)

    await msg.answer_document(FSInputFile(filepath), caption="✅ Campaigns exported.")
  
