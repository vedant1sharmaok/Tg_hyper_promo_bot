from aiogram import Router, types, F
from aiogram.filters import Command
from services.ai_tools import generate_promo, translate_text, generate_variations, basic_spam_score

router = Router()

@router.message(commands("ai_write"))
async def ai_writer(msg: types.Message):
    await msg.answer("🧠 What’s your promo topic?")

    @router.message()
    async def receive_topic(inner: types.Message):
        topic = inner.text.strip()
        await inner.answer("⚙️ Generating...")
        text = await generate_promo(topic)
        await inner.answer(f"✅ Here's a promo:\n\n{text}")

@router.message(commands("ai_translate"))
async def ai_translate(msg: types.Message):
    await msg.answer("🌐 Send the text to translate (reply) and language code (e.g., Hindi):")

    @router.message()
    async def receive_translation(inner: types.Message):
        parts = inner.text.strip().split("\n", 1)
        if len(parts) < 2:
            return await inner.answer("⚠️ Format: `language`\n`text`")
        lang, text = parts[0], parts[1]
        translated = await translate_text(text, lang)
        await inner.answer(f"🈶 Translated:\n\n{translated}")

@router.message(commands("ai_variation"))
async def ai_variation(msg: types.Message):
    await msg.answer("🔁 Send a message to generate 3 variations:")

    @router.message()
    async def receive_var(inner: types.Message):
        base = inner.text.strip()
        variations = await generate_variations(base)
        await inner.answer(f"🔁 Variations:\n\n{variations}")

@router.message(commands("ai_score"))
async def ai_score(msg: types.Message):
    await msg.answer("🧪 Send a promo message to check spam score:")

    @router.message()
    async def spam_check(inner: types.Message):
        text = inner.text.strip()
        score, words = basic_spam_score(text)
        await inner.answer(f"📊 Spam Score: {score}/7\nTrigger words: {', '.join(words)}")
  
