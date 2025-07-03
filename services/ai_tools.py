import openai
from config import OPENAI_KEY

openai.api_key = OPENAI_KEY

async def generate_promo(topic):
    prompt = f"Write a short and catchy promotional message about: {topic}"
    res = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content.strip()

async def translate_text(text, target_lang):
    prompt = f"Translate this to {target_lang}:\n\n{text}"
    res = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content.strip()

async def generate_variations(base_text):
    prompt = f"Give me 3 alternate versions of this promo message:\n\n{base_text}"
    res = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content.strip()

def basic_spam_score(text):
    spam_words = ["free", "win", "click", "guaranteed", "offer", "bonus", "act now"]
    score = sum(word in text.lower() for word in spam_words)
    return score, spam_words
  
