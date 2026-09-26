import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
from connector import create_tables
import services

load_dotenv()

TOKEN = os.getenv("BOT")

bot = Bot(token=TOKEN)
dp = Dispatcher()

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🐾 Мои питомцы"),
            KeyboardButton(text="📋 Добавить событие")
        ],
    ],
    resize_keyboard=True
)

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("""
            Бот для владельцев домашних животных\n
/add_pet - Добавляет нового питомца пользователю\n
/my_pets - Показывает всех питомцев пользователя\n
/log_care - Записывает событие ухода (feeding / vet_visit / vaccination)\n
/pet_history - Показывает последние 10 событий по питомцу\n
/last_vaccination - Показывает дату последней прививки этого питомца 

        """,
        reply_markup=keyboard
    )

async def main():
    await create_tables()
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


