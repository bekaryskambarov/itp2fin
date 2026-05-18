import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# IMPORTING YOUR MODULES
from database import DatabaseManager
from utils import calculate_nearest_places, format_feedback

# 1. INITIALIZATION
BOT_TOKEN = "8734845651:AAFdQWfsYT9XfM7JqqDpobcSMfYdSMRzsXo"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
db = DatabaseManager()

# Combined list of all 60 locations for the "Nearest" search
from data_store import RESTAURANTS, LIBRARIES, PARKS  # Suggested: keep data in a separate file too

ALL_LOCATIONS = RESTAURANTS + LIBRARIES + PARKS


class BotStates(StatesGroup):
    waiting_for_feedback = State()


# 2. KEYBOARDS (Modular approach)
def get_main_kb():
    return types.ReplyKeyboardMarkup(keyboard=[
        [types.KeyboardButton(text="📍 Nearest 5 Places", request_location=True)],
        [types.KeyboardButton(text="🍴 Restaurants"), types.KeyboardButton(text="🌳 Parks")],
        [types.KeyboardButton(text="📚 Libraries"), types.KeyboardButton(text="👨‍💻 Developers")]
    ], resize_keyboard=True)


# 3. HANDLERS
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Welcome to the Professional Astana Guide! 🏙", reply_markup=get_main_kb())


@dp.message(F.location)
async def handle_location(message: types.Message):
    # Use Utility to find nearest
    nearest = calculate_nearest_places(
        message.location.latitude,
        message.location.longitude,
        ALL_LOCATIONS
    )

    response = "🌟 **Top 5 Nearest Cool Places:**\n\n"
    for i, p in enumerate(nearest, 1):
        response += f"{i}. **{p['name']}** ({p['distance']:.2f} km)\n_{p['desc']}_\n\n"

    await message.answer(response, parse_mode="Markdown")
    # Show the absolute closest on map
    await message.answer_location(latitude=nearest[0]['lat'], longitude=nearest[0]['lon'])


@dp.callback_query(F.data.startswith("write_"))
async def start_feedback(call: types.CallbackQuery, state: FSMContext):
    # Logic to save place name in state
    place_name = call.data.split("_")[1]
    await state.update_data(place_name=place_name)
    await call.message.answer(f"Writing review for {place_name}. Please type:")
    await state.set_state(BotStates.waiting_for_feedback)


@dp.message(BotStates.waiting_for_feedback)
async def save_feedback(message: types.Message, state: FSMContext):
    data = await state.get_data()
    # Use Database Module to save
    db.add_review(data['place_name'], message.text)
    await message.answer("✅ Review saved to database!")
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())