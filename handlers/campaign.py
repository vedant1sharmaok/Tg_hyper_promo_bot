from aiogram import Router, types, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from services.campaigns import save_campaign, get_user_campaigns, update_campaign_status

router = Router()

class CampaignState(StatesGroup):
    name = State()
    text = State()
    media = State()
    groups = State()
    accounts = State()
    delay_group = State()
    delay_message = State()

temp_campaign_data = {}

@router.message(commands="new_campaign")
async def new_campaign(msg: types.Message, state: FSMContext):
    await msg.answer("📛 Enter campaign name:")
    await state.set_state(CampaignState.name)

@router.message(CampaignState.name)
async def get_name(msg: types.Message, state: FSMContext):
    temp_campaign_data[msg.from_user.id] = {"name": msg.text.strip()}
    await msg.answer("📝 Enter the message text:")
    await state.set_state(CampaignState.text)

@router.message(CampaignState.text)
async def get_text(msg: types.Message, state: FSMContext):
    temp_campaign_data[msg.from_user.id]["text"] = msg.text.strip()
    await msg.answer("📎 Send an image/video/document for media or /skip:")
    await state.set_state(CampaignState.media)

@router.message(CampaignState.media, F.content_type.in_({"photo", "video", "document"}))
async def get_media(msg: types.Message, state: FSMContext, bot):
    file_id = msg.photo[-1].file_id if msg.photo else msg.document.file_id if msg.document else msg.video.file_id
    file = await bot.get_file(file_id)
    media_path = f"static/media/{file_id}"
    await bot.download_file(file.file_path, destination=media_path)
    temp_campaign_data[msg.from_user.id]["media_path"] = media_path
    await msg.answer("📮 Enter target group usernames separated by commas:")
    await state.set_state(CampaignState.groups)

@router.message(CampaignState.media, F.text.lower() == "/skip")
async def skip_media(msg: types.Message, state: FSMContext):
    temp_campaign_data[msg.from_user.id]["media_path"] = None
    await msg.answer("📮 Enter target group usernames separated by commas:")
    await state.set_state(CampaignState.groups)

@router.message(CampaignState.groups)
async def get_groups(msg: types.Message, state: FSMContext):
    groups = [g.strip() for g in msg.text.split(",") if g.strip()]
    temp_campaign_data[msg.from_user.id]["target_groups"] = groups
    await msg.answer("👤 Enter account IDs to use (comma-separated or /all):")
    await state.set_state(CampaignState.accounts)

@router.message(CampaignState.accounts)
async def get_accounts(msg: types.Message, state: FSMContext):
    accounts = msg.text.strip()
    if accounts == "/all":
        account_ids = []  # Will assign all user’s accounts later
    else:
        account_ids = [a.strip() for a in accounts.split(",") if a.strip()]
    temp_campaign_data[msg.from_user.id]["accounts_used"] = account_ids
    await msg.answer("⏱️ Enter delay between groups (seconds):")
    await state.set_state(CampaignState.delay_group)

@router.message(CampaignState.delay_group)
async def get_group_delay(msg: types.Message, state: FSMContext):
    try:
        temp_campaign_data[msg.from_user.id]["interval_between_groups"] = int(msg.text.strip())
        await msg.answer("⏳ Enter delay between messages in a group (seconds):")
        await state.set_state(CampaignState.delay_message)
    except:
        await msg.answer("⚠️ Please enter a valid number")

@router.message(CampaignState.delay_message)
async def get_msg_delay(msg: types.Message, state: FSMContext):
    try:
        temp_campaign_data[msg.from_user.id]["interval_between_messages"] = int(msg.text.strip())
        data = temp_campaign_data.pop(msg.from_user.id)
        await save_campaign(
            msg.from_user.id,
            data["name"], data["text"], data["media_path"],
            data["target_groups"], data["accounts_used"],
            data["interval_between_groups"], data["interval_between_messages"]
        )
        await msg.answer("✅ Campaign saved and activated!")
        await state.clear()
    except Exception as e:
        await msg.answer(f"⚠️ Error saving campaign: {str(e)}")
                   
