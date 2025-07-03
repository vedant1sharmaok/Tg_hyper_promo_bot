from database import db

accounts_col = db.accounts

async def save_account(user_id, session_str, phone, username, is_active=True):
    await accounts_col.insert_one({
        "owner_id": user_id,
        "session_string": session_str,
        "phone": phone,
        "username": username,
        "active": is_active
    })

async def get_user_accounts(user_id):
    return await accounts_col.find({"owner_id": user_id}).to_list(length=100)
