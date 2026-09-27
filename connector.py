import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

async def get_connection():
    return await asyncpg.connect(
        user="postgres",
        password=os.getenv("PASSWORD_DB"),
        database="exam_pet",   
        host="localhost",
        port=5432
    )

async def create_tables():
    conn = None
    try:
        conn = await get_connection()
        await conn.execute("""
            CREATE TABLE if not exists pets(
                id SERIAL PRIMARY KEY,
                user_id BIGINT,
                name VARCHAR(100),
                species VARCHAR(100)
            )
        """)
        await conn.execute("""
            CREATE TABLE if not exists care_logs(
                id SERIAL PRIMARY KEY,
                pet_id INT REFERENCES pets(id) ON DELETE CASCADE,
                type VARCHAR(100),
                logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Таблицы успешно созданы")
    except Exception as error:
        print("Ошибка:", error)
    finally:
        if conn:
            await conn.close()