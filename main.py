from BotCreator import dp
from aiogram.utils import executor
import logging
from handlers import client, states
from database import sqlite_db

logging.basicConfig(level=logging.INFO)
sqlite_db.sql_start()

client.reg_handlers(dp)
states.reg_handlers_admin(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)