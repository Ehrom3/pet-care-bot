import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart,CommandObject
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import StatesGroup , State
from dotenv import load_dotenv
from connector import create_tables
from services import *


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

@dp.message(Command("my_pets"))
@dp.message(F.text == "🐾 Мои питомцы")
async def my_pets(message: Message):
    user_id = message.from_user.id
    pets = await get_my_pets(user_id)

    if not pets:
        await message.answer("🐾 У вас пока нет питомцев.")
        return

    text = "🐾 Ваши питомцы:\n\n"

    for pet in pets:
        text += (
            f"🆔 {pet['id']}\n"
            f"Имя: {pet['name']}\n"
            f"Вид: {pet['species']}\n\n"
        )
    await message.answer(text)

@dp.message(F.text == "📋 Добавить событие")
async def care_button(message: Message):
    await message.answer(
        "📋 Используйте команду:\n"
        "/log_care <pet_id> <тип>\n\n"
        "Допустимые типы:\n"
        "🍖 feeding  -  «кормление»\n"
        "🏥 vet_visit  -  «визит к ветеринару» \n"
        "💉 vaccination  -  «вакцинация » \n\n"
        "Пример: /log_care 1 vaccination"
    )

@dp.message(Command("log_care"))
async def log_care(message: Message, command: CommandObject):
    if not command.args:
        await message.answer(
        "📋 Используйте команду:\n"
        "/log_care <pet_id> <тип>\n\n"
        "Допустимые типы:\n"
        "🍖 feeding  -  «кормление»\n"
        "🏥 vet_visit  -  «визит к ветеринару» \n"
        "💉 vaccination  -  «вакцинация » \n\n"
        "Пример: /log_care 1 vaccination"
    )
        return
    args = command.args.split()
    if len(args) != 2:
        await message.answer("❌ Пример: /log_care 1 vaccination")
        return
    try:
        pet_id = int(args[0])
    except Exception:
        await message.answer("❌ pet_id должен быть числом.")
        return

    care_type = args[1].lower()
    allowed_types = ["feeding", "vet_visit", "vaccination"]
    if care_type not in allowed_types:
        await message.answer(
            "❌ Неверный тип события.\n\n"
            "Допустимые типы:\n"
            "🍖 feeding\n"
            "🏥 vet_visit\n"
            "💉 vaccination"
        )
        return

    user_id = message.from_user.id
    pet = await check_pet(pet_id, user_id)
    if not pet:
        await message.answer("❌ Питомец не найден или принадлежит другому пользователю.")
        return

    await care_add(pet_id, care_type)
    await message.answer(
        f"✅ Событие добавлено!\n"
        f"🐾 Питомец: {pet['name']}\n"
        f"📋 Тип: {care_type}"
    )

@dp.message(Command("pet_history"))
async def pet_history(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("❌ Используйте: /pet_history <pet_id>")
        return

    try:
        pet_id = int(command.args)
    except Exception:
        await message.answer("❌ pet_id должен быть числом.")
        return

    user_id = message.from_user.id
    pet = await check_pet(pet_id, user_id)
    if not pet:
        await message.answer("❌ Питомец не найден или принадлежит другому пользователю.")
        return

    history = await get_pet_history(pet_id)
    if not history:
        await message.answer(f"📋 У питомца {pet['name']} пока нет истории ухода.")
        return

    text = f"📋 История ухода — {pet['name']}:\n\n"
    for row in history:
        text += (
            f"🔹 {row['type']}\n"
            f"🕐 {row['logged_at'].strftime('%d.%m.%Y %H:%M')}\n\n"
        )
    await message.answer(text)




async def main():
    await create_tables()
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


