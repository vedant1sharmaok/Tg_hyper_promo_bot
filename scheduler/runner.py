import asyncio
from datetime import datetime
from app.database import db
from app.services.dispatcher import dispatch_campaign

campaigns_col = db.campaigns

async def scheduler_loop():
    while True:
        active_campaigns = await campaigns_col.find({"status": "active"}).to_list(100)
        for campaign in active_campaigns:
            asyncio.create_task(dispatch_campaign(campaign))
        await asyncio.sleep(60)  # Check every 60 seconds
