import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart,CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup , State
from dotenv import load_dotenv
from connector import create_tables
from services import pet_add


load_dotenv()

TOKEN = os.getenv("BOT")

bot = Bot(token=TOKEN)
dp = Dispatcher()
pet_data={}

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🐾 Мои питомцы"),
            KeyboardButton(text="📋 Добавить событие")
        ],
    ],
    resize_keyboard=True
)


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "🐾Бот для владельцев домашних животных!\n\n"
"/add_pet - Добавляет нового питомца пользователю\n"
"/my_pets - Показывает всех питомцев пользователя\n"
"/log_care - Записывает событие ухода (feeding / vet_visit / vaccination)\n"
"/pet_history - Показывает последние 10 событий по питомцу\n"
"/last_vaccination - Показывает дату последней прививки этого питомца"
    ,reply_markup=keyboard
    )

@dp.message(Command("add_pet"))
async def add_pet(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("❌ Используйте: /add_pet <имя> <вид>")
        return
    args = command.args.split(maxsplit=1)
    if len(args) != 2:
        await message.answer("❌ Укажите имя и вид.\nПример: /add_pet Барсик cat")
        return

    name = args[0]
    species = args[1]
    user_id = message.from_user.id

    await pet_add(user_id, name, species)
    await message.answer(
        f"✅ Питомец добавлен!\n"
        f"🐾 Имя: {name}\n"
        f"🐶 Вид: {species}"
    )


async def main():
    await create_tables()
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


