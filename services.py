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

