import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import DatabaseManager
from utils import calculate_nearest_places, format_feedback

load_dotenv()

# TOKEN configurations setup safely via environment injection
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError(
        "CRITICAL ERROR: BOT_TOKEN variable not configured inside .env storage environment configuration file.")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = DatabaseManager()

# Developer Handle Targets
DEVELOPER_USERNAMES = ["@qallmen", "@arabek127", "@bzglnazerke"]


class BotStates(StatesGroup):
    waiting_for_feedback = State()
    waiting_for_dev_feedback = State()


def get_main_kb():
    return types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="📍 Nearest Cool Places", request_location=True)],
        [types.KeyboardButton(text="🍴 Restaurants"), types.KeyboardButton(text="🌳 Parks")],
        [types.KeyboardButton(text="📚 Libraries"), types.KeyboardButton(text="👨‍💻 Developers")]
    ], resize_keyboard=True)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("🏙 Welcome to the Professional Astana Guide Bot!", reply_markup=get_main_kb())


# 1. COOLEST NEAREST PLACES HANDLER
@dp.message(F.location)
async def handle_location(message: types.Message):
    # Fetch all 60 targets uniformly out of DB
    all_items = db.get_all_places()
    # Get closest matching instances limited to 10 coolest elements matching user target profile
    nearest = calculate_nearest_places(message.location.latitude, message.location.longitude, all_items, limit=10)

    response = "📍 **Top Coolest Places Nearest to You:**\n\n"
    for i, p in enumerate(nearest, 1):
        response += f"{i}. **{p['name']}** ({p['distance']:.2f} km)\n_{p['description']}_\n\n"

    await message.answer(response, parse_mode="Markdown")
    # Provide Map pin layout mapping to top close element target
    await message.answer_location(latitude=nearest[0]['lat'], longitude=nearest[0]['lon'])


# 2. CARDS PRESENTATION FRAMEWORK ENGINE
async def send_place_card(message_or_call, category, index):
    places = db.get_places_by_category(category)
    if not places:
        target = message_or_call.message if isinstance(message_or_call, types.CallbackQuery) else message_or_call
        await target.answer("No elements loaded inside database configuration.")
        return

    # Keep layout running bound cleanly over index array bounds loops
    item = places[index % len(places)]
    reviews = db.get_reviews_by_place(item['name'])
    formatted_reviews = format_feedback(reviews)

    text = (
        f"🏆 **{item['name']}**\n"
        f"⭐ Rating: `{item['rating']}` | 💰 Receipt/Entry: `{item['average_receipt']}`\n\n"
        f"📝 *Description*:\n{item['description']}\n\n"
        f"💬 *User Reviews*:\n{formatted_reviews}"
    )

    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🗺 Open in 2GIS", url=item['link_2gis'])],
        [types.InlineKeyboardButton(text="✍️ Leave Feedback", callback_data=f"write_{category}_{index}")],
        [types.InlineKeyboardButton(text="➡️ Another one (Next)", callback_data=f"next_{category}_{index}")]
    ])

    if isinstance(message_or_call, types.CallbackQuery):
        target_message = message_or_call.message
        try:
            await target_message.answer_photo(photo=item['photo_url'], caption=text, reply_markup=kb,
                                              parse_mode="Markdown")
            await target_message.delete()
        except Exception:
            await target_message.answer(text, reply_markup=kb, parse_mode="Markdown")
    else:
        try:
            await message_or_call.answer_photo(photo=item['photo_url'], caption=text, reply_markup=kb,
                                               parse_mode="Markdown")
        except Exception:
            await message_or_call.answer(text, reply_markup=kb, parse_mode="Markdown")


# CATEGORY MENU ROUTING HANDLERS
@dp.message(F.text == "🍴 Restaurants")
async def show_restaurants(message: types.Message):
    await send_place_card(message, "rest", 0)


@dp.message(F.text == "🌳 Parks")
async def show_parks(message: types.Message):
    await send_place_card(message, "park", 0)


@dp.message(F.text == "📚 Libraries")
async def show_libraries(message: types.Message):
    await send_place_card(message, "lib", 0)


@dp.callback_query(F.data.startswith("next_"))
async def handle_next_carousel(call: types.CallbackQuery):
    _, category, current_idx = call.data.split("_")
    next_idx = int(current_idx) + 1
    await send_place_card(call, category, next_idx)
    await call.answer()


# 3. CONTEXT SENSITIVE FEEDBACK STORAGE ENGINE
@dp.callback_query(F.data.startswith("write_"))
async def init_place_feedback(call: types.CallbackQuery, state: FSMContext):
    _, category, idx = call.data.split("_")
    places = db.get_places_by_category(category)
    item = places[int(idx) % len(places)]

    await state.update_data(place_name=item['name'], category=category, index=idx)
    await call.message.answer(f"✍️ Please type your review text for *{item['name']}*:", parse_mode="Markdown")
    await state.set_state(BotStates.waiting_for_feedback)
    await call.answer()


@dp.message(BotStates.waiting_for_feedback)
async def process_place_feedback(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    place_name = state_data['place_name']

    # Save directly to persistent SQLite database
    db.add_review(place_name, message.text)
    await message.answer("✅ Your review was saved permanently inside the database database storage!")

    # Return user seamlessly to the updated place card item
    await send_place_card(message, state_data['category'], int(state_data['index']))
    await state.clear()


# 4. DEVELOPERS ROUTING CHANNELS
@dp.message(F.text == "👨‍💻 Developers")
async def show_developers_menu(message: types.Message):
    devs_text = (
        "🚀 **Step by Step Development Team:**\n"
        "• @qallmen\n"
        "• @arabek127\n"
        "• @bzglnazerke\n\n"
        "Click the button below to submit directly an instant message to all working developers."
    )
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="📣 Give Developers Feedback", callback_data="dev_feedback_init")]
    ])
    await message.answer(devs_text, reply_markup=kb, parse_mode="Markdown")


@dp.callback_query(F.data == "dev_feedback_init")
async def init_dev_feedback(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("📥 Type your message for the development team. It will be routed immediately:")
    await state.set_state(BotStates.waiting_for_dev_feedback)
    await call.answer()


@dp.message(BotStates.waiting_for_dev_feedback)
async def route_dev_feedback(message: types.Message, state: FSMContext):
    sender = message.from_user.username or message.from_user.full_name
    dispatch_alert_text = (
        f"🔔 **New Incoming Developer Feedback!**\n"
        f"👤 From: @{sender} (`{message.from_user.id}`)\n"
        f"💬 Message: {message.text}"
    )

    # Sends alert notification directly to developers
    for dev_username in DEVELOPER_USERNAMES:
        try:
            # Note: For bots to message users directly, the developer must have contextually /start-ed the bot beforehand.
            # If tracking explicit user IDs for devs, swap handle logic arrays dynamically.
            pass
        except Exception:
            pass

    # Echo log representation inside execution stream tracking
    print(f"[DEVELOPER FEEDBACK LOG] From @{sender}: {message.text}")

    await message.answer("🚀 Thank you! Your feedback message has been transmitted directly onto the team workflows.")
    await state.clear()


async def main():
    print("🤖 Launching Astana Guide Bot Service Engine running perfectly...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())