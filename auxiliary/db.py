import aiosqlite
import config
from loguru import logger

DB_NAME = config.DB_NAME

import auxiliary.messages as messages


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS users (" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT," \
            "username TEXT UNIQE," \
            "name TEXT," \
            "age INTEGER," \
            "email TEXT," \
            "tel TEXT," \
            "isAdmin INTEGER)"
        )

        await db.execute(
            "CREATE TABLE IF NOT EXISTS slots (" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT," \
            "date TEXT," \
            "time TEXT," \
            "new INTEGER)"
        )

        await db.execute(
            "CREATE TABLE IF NOT EXISTS apointments (" \
            "id INTEGER PRIMARY KEY AUTOINCREMENT," \
            "date TEXT," \
            "time TEXT," \
            "userID INTEGER," \
            "new INTEGER)"
        )
        
        await db.commit()
        logger.info(f'{messages.DB_INITIALIZED}')
    
async def get_items(table: str):
    """The function gets all records from the specified table and returns them as a tuple of list"""
    async with aiosqlite.connect(DB_NAME) as db:
        items = await db.execute(f"SELECT * FROM {table}")
        result = await items.fetchall()
        return result
