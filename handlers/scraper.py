from aiogram import Router, types, F
from app.services.group_scraper import search_public_groups
from app.services.accounts import get_user_accounts

router = Router()

@router.message(commands="scrape_groups")
async def scrape_groups(msg: types.Message):
    accounts = await get_user_accounts(msg.from_user.id)
    if not accounts:
        return await msg.answer("🔐 You must add an account first using /add_account")

    session = accounts[0]["session_string"]
    await msg.answer("🔎 Enter keyword to search public groups:")

    @router.message()
    async def keyword_response(m: types.Message):
        keyword = m.text.strip()
        await m.answer(f"🔍 Searching for public groups with '{keyword}'...")

        try:
            groups = await search_public_groups(session, keyword)
            if not groups:
                return await m.answer("❌ No groups found or not accessible.")

            text = "🔎 Found Groups:\n\n"
            for i, g in enumerate(groups, 1):
                text += f"{i}. {g['name']} (@{g['username']}) — 👥 {g['members']} members\n"

            await m.answer(text + "\nReply with group numbers (comma-separated) to save.")

            @router.message()
            async def select_groups(m2: types.Message):
                try:
                    nums = [int(n.strip()) for n in m2.text.split(",")]
                    selected = [groups[n - 1]["username"] for n in nums]
                    await m2.answer(f"✅ Selected: {', '.join(selected)}\nYou can now add them to a campaign.")
                except:
                    await m2.answer("⚠️ Invalid input. Try numbers separated by commas (e.g., 1, 3, 4)")

        except Exception as e:
            await m.answer(f"⚠️ Error: {str(e)}")
                  
