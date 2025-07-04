from aiogram import Router, types, F
from aiogram.filters import Command
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

@router.message(Command("add_account"))
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

@router.message(Command("my_accounts"))
async def show_accounts(msg: types.Message):
    accounts = await get_user_accounts(msg.from_user.id)
    if not accounts:
        return await msg.answer("📭 No accounts linked yet.")
    text = "\n".join([f"📱 {a['phone']} | @{a.get('username', 'unknown')}" for a in accounts])
    await msg.answer(f"🔐 Your Accounts:\n{text}")
@router.message(Command("add_account"))
async def add_account_cmd(msg: types.Message, state: FSMContext):
    await state.set_state(AccountStates.waiting_for_session)
    await msg.answer("📱 Send your Telethon session string:")

@router.message(AccountStates.waiting_for_session)
async def session_step(msg: types.Message, state: FSMContext):
    await state.update_data(session=msg.text)
    await msg.answer("🌐 Enter proxy in format:\n`type:host:port:username:password`\n\nExample:\nsocks5:127.0.0.1:1080:user:pass\nSend `skip` to add without proxy.")
    await state.set_state(AccountStates.waiting_for_proxy)

@router.message(AccountStates.waiting_for_proxy)
async def proxy_step(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    proxy_text = msg.text.strip()
    proxy = None

    if proxy_text.lower() != "skip":
        try:
            ptype, host, port, user, pw = proxy_text.split(":")
            proxy = {
                "type": ptype,
                "addr": host,
                "port": int(port),
                "username": user,
                "password": pw
            }
        except:
            return await msg.answer("⚠️ Invalid proxy format.")

    await accounts_col.insert_one({
        "session_string": data["session"],
        "owner_id": msg.from_user.id,
        "proxy": proxy,
        "phone": "unknown"
    })

    await msg.answer("✅ Account added successfully with proxy!" if proxy else "✅ Account added without proxy.")
    await state.clear()
        
__all__ = ["router"]
                    
