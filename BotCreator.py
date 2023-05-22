from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token='6232187526:AAEpuA62SW_YE0KMT_oVN9Fhw0uXu5TgxLI', parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)