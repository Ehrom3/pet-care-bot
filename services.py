from connector import get_connection


async def pet_add(user_id, name, species):
    con = await get_connection()
    await con.execute("""
        INSERT INTO pets (user_id, name, species) 
        VALUES ($1, $2, $3)
        """, user_id, name, species)
    await con.close()

async def get_my_pets(user_id):
    con = await get_connection()
    rows = await con.fetch("""
        SELECT id, name, species FROM pets 
        WHERE user_id = $1 ORDER BY id
        """, user_id)
    await con.close()
    return rows

async def check_pet(pet_id, user_id):
    con = await get_connection()
    pet = await con.fetchrow("""
        SELECT id, name, species FROM pets 
        WHERE id = $1 AND user_id = $2
        """, pet_id, user_id)
    await con.close()
    return pet

async def care_add(pet_id, care_type):
    con = await get_connection()
    await con.execute("""
        INSERT INTO care_logs (pet_id, type) VALUES ($1, $2)
        """, pet_id, care_type)
    await con.close()

async def get_pet_history(pet_id):
    con = await get_connection()
    rows = await con.fetch("""
        SELECT type, logged_at FROM care_logs 
        WHERE pet_id = $1 ORDER BY logged_at DESC LIMIT 10
        """, pet_id)
    await con.close()
    return rows

async def get_last_vaccination(pet_id):
    con = await get_connection()
    row = await con.fetchrow("""
        SELECT logged_at FROM care_logs
        WHERE pet_id = $1 AND type = 'vaccination' ORDER BY logged_at DESC LIMIT 1
        """, pet_id)
    await con.close()
    return row

@dp.message(Command("last_vaccination"))
async def last_vaccination(message: Message, command: CommandObject):
    if not command.args:
        await message.answer("❌ Используйте: /last_vaccination <pet_id>")
        return

    try:
        pet_id = int(command.args)
    except ValueError:
        await message.answer("❌ pet_id должен быть числом.")
        return

    user_id = message.from_user.id
    pet = await check_pet(pet_id, user_id)
    if not pet:
        await message.answer("❌ Питомец не найден или принадлежит другому пользователю.")
        return

    vaccination = await get_last_vaccination(pet_id)
    if not vaccination:
        await message.answer(f"💉 У питомца {pet['name']} прививок ещё не было.")
        return

    await message.answer(
        f"💉 Последняя прививка — {pet['name']}\n"
        f"📅 {vaccination['logged_at'].strftime('%d.%m.%Y %H:%M')}"
    )

