from fastapi import Header, HTTPException

API_KEYS = {
    "demo_user_token": 123456789  # token: telegram_user_id mapping
}

async def get_user_from_token(x_api_key: str = Header(...)):
    if x_api_key not in API_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return API_KEYS[x_api_key]
  
