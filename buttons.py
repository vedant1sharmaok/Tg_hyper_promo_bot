from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def format_buttons(language="en"):
    if language == "hi":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="शुरू करें", callback_data="start_campaign")],
            [InlineKeyboardButton(text="सहायता", callback_data="help")],
        ])
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Start", callback_data="start_campaign")],
        [InlineKeyboardButton(text="Help", callback_data="help")],
    ])
  
