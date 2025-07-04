from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from database import campaigns_col
import json
import os

router = Router()

@router.message(Command("export_campaigns"))
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
  
@router.message(Command("import_campaigns"))
async def import_campaigns(msg: types.Message):
    await msg.answer("📥 Send your JSON export file to import campaigns.")

@router.message(F.document)
async def handle_import_file(msg: types.Message):
    if not msg.document.file_name.endswith(".json"):
        return await msg.answer("❌ Please upload a valid JSON file.")

    file_path = f"static/imports/{msg.document.file_name}"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    await msg.bot.download(msg.document, destination=file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            for camp in data:
                camp["owner_id"] = msg.from_user.id
                await campaigns_col.insert_one(camp)
            await msg.answer("✅ Campaigns imported successfully!")
        except Exception as e:
            await msg.answer(f"⚠️ Failed to import: {str(e)}")
        
