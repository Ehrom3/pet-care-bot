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

