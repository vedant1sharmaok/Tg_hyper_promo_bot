import json
import os
from database import users_col

LANG_PATH = "locales"

_cache = {}

def load_language(lang_code):
    if lang_code in _cache:
        return _cache[lang_code]
    file_path = os.path.join(LANG_PATH, f"{lang_code}.json")
    if not os.path.exists(file_path):
        file_path = os.path.join(LANG_PATH, "en.json")
    with open(file_path, "r", encoding="utf-8") as f:
        _cache[lang_code] = json.load(f)
    return _cache[lang_code]

async def get_lang(user_id):
    user = await users_col.find_one({"telegram_id": user_id})
    lang_code = user.get("language", "en")
    return load_language(lang_code)
