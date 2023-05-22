import sqlite3
from BotCreator import bot
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


def sql_start():
    global base, cursor
    base = sqlite3.connect('Messages.db')
    cursor = base.cursor()
    if base:
        print('Data base connected!')
        base.execute(
            "CREATE TABLE IF NOT EXISTS messages(img TEXT, message TEXT PRIMARY KEY)")
        base.commit()


async def sql_add_commands(state):
    async with state.proxy() as data:
            cursor.execute("INSERT INTO messages VALUES (?,?)", tuple(data.values()))
            base.commit()


async def sql_read(answer: Message):
    for i in cursor.execute("SELECT * FROM messages").fetchall():
        photo = str(i[0])
        message = str(i[1])
        await bot.send_photo(answer.from_user.id, photo, f'Message: {message}',
                             reply_markup=InlineKeyboardMarkup().add(
                                 InlineKeyboardButton(text='broadcast ✉️', callback_data=f'done {message}')))


async def sql_read_as_list():
    return cursor.execute('SELECT * FROM messages').fetchall()


async def sql_deleter(item):
    cursor.execute('DELETE FROM messages WHERE message == ?', (item,))
    base.commit()


async def find_item(item):
    cursor.execute(f'SELECT * FROM messages WHERE message == {item}')


