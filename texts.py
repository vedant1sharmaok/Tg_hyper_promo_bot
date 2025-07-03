TEXTS = {
    "en": {
        "start": "Welcome to the TG Hyper Promo Bot!",
        "help": "This bot helps you manage promotional campaigns.",
        "error": "An error occurred: ",
    },
    "hi": {
        "start": "TG हाइपर प्रमोशन बॉट में आपका स्वागत है!",
        "help": "यह बॉट प्रचार अभियानों को प्रबंधित करता है।",
        "error": "एक त्रुटि हुई: ",
    }
}

def get_text(lang: str, key: str) -> str:
    return TEXTS.get(lang, TEXTS["en"]).get(key, key)
  
