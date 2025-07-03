def format_campaign_info(campaign):
    return (
        f"📢 Campaign: {campaign['name']}\\n"
        f"💬 Message: {campaign['message'][:50]}...\\n"
        f"📆 Interval: {campaign['interval']}s\\n"
        f"🧾 Accounts: {len(campaign['accounts'])}"
    )
  
