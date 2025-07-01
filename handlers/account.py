from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from app.clients.telethon_client import login_with_otp
from app.services.accounts import save_account, get_user_accounts

router = Router()

class LoginState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_otp = State()
    waiting_for_password = State()

user_login_data = {}

@router.message(commands="add_account")
async def start_login(msg: types.Message, state: FSMContext):
    await msg.answer("📱 Enter your phone number (with country code):")
    await state.set_state(LoginState.waiting_for_phone)

@router.message(LoginState.waiting_for_phone)
async def get_phone(msg: types.Message, state: FSMContext):
    phone = msg.text.strip()
    user_login_data[msg.from_user.id] = {"phone": phone}

    async def otp_input():
        await msg.answer("📩 Enter the OTP sent to your Telegram:")
        otp_msg = await state.wait_for_message()
        return otp_msg.text.strip()

    async def pass_input():
        await msg.answer("🔐 Enter your 2FA password:")
        pass_msg = await state.wait_for_message()
        return pass_msg.text.strip()

    try:
        session_str, user = await login_with_otp(phone, otp_input, pass_input)
        await save_account(msg.from_user.id, session_str, phone, user.username or "unknown")
        await msg.answer(f"✅ Account {user.first_name} added successfully.")
    except Exception as e:
        await msg.answer(f"❌ Failed to login: {str(e)}")
    finally:
        await state.clear()

@router.message(commands="my_accounts")
async def show_accounts(msg: types.Message):
    accounts = await get_user_accounts(msg.from_user.id)
    if not accounts:
        return await msg.answer("📭 No accounts linked yet.")
    text = "\n".join([f"📱 {a['phone']} | @{a.get('username', 'unknown')}" for a in accounts])
    await msg.answer(f"🔐 Your Accounts:\n{text}")
