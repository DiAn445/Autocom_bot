import asyncio
import random
import httpx
from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from BotCreator import bot, dp
from aiogram.dispatcher.filters import Text
from database import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ID = None


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def if_admin(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'ready to work!', reply_markup=admin_kb.button_case_admin)


async def cancel_state(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('canceled')


async def uploader(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('upload photo:')


async def upload_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply('input message:')


async def input_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        if message.text == '/cancel':
            await cancel_state(message, state)
            return
        async with state.proxy() as data:
            data['text'] = message.text
        async with state.proxy() as data:
            await message.reply(str(data))
        await sqlite_db.sql_add_commands(state)
        await state.finish()


async def del_callback_command(callback_query: types.CallbackQuery):
    await sqlite_db.sql_deleter(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f"{callback_query.data.replace('del ', '')} deleted!", show_alert=True)


async def delete_item(item: types.Message):
    if item.from_user.id == ID:
        read = await sqlite_db.sql_read_as_list()
        if read:
            try:
                for i in read:
                    await bot.send_photo(item.from_user.id, i[0], f'{i[1]}',
                                         reply_markup=InlineKeyboardMarkup().add(
                                             InlineKeyboardButton(text=f"Delete: {i[1]}", callback_data=f"del {i[1]}")))
                await item.delete()
            except:
                pass
        else:
            await bot.send_message(item.from_user.id, 'nothing to delete!')


proxy_list = [
    '5.78.106.1:8080',
    '159.223.119.107:8080',
    '5.161.62.204:8080',
    '5.161.222.66:8080',
    '5.161.228.93:8080',
    '5.161.220.130:8080'
]


async def auto_comment(user_id: int, res):
    chat_ids = [-1001755215712, 580940559]  # Chat ID list

    max_messages_per_day = 8400
    max_chats_per_round = len(chat_ids)
    rounds_per_day = 4
    messages_sent = 0
    proxy_index = 0

    for current_round in range(1, rounds_per_day + 1):
        res = res if len(res) == 1 else [await asyncio.to_thread(random.choice, res)]

        if messages_sent >= max_messages_per_day:
            break

        for chat_id in chat_ids:
            if messages_sent >= max_messages_per_day:
                break

            proxy = proxy_list[proxy_index]
            print(f"Working with proxy: {proxy}")

            async with httpx.AsyncClient(proxies=f"socks5://{proxy}") as client:
                try:
                    print(f"Sending message to chat ID: {chat_id}")
                    await bot.send_photo(chat_id=chat_id, photo=str(res[0][0]), caption=str(res[0][1]))
                    messages_sent += 1
                    print(f"Messages sent: {messages_sent}/{max_messages_per_day}")

                    delay = random.uniform(2, 5)
                    await asyncio.sleep(delay)

                    if messages_sent % 5 == 0:
                        proxy_index = (proxy_index + 1) % len(proxy_list)
                        print("Changing proxy...")

                    if messages_sent % max_chats_per_round == 0:
                        delay = random.randint(7200, 10800)
                        print(f"Waiting for {delay} seconds before the next round.")
                        await asyncio.sleep(delay)

                    if messages_sent % (max_messages_per_day // rounds_per_day // max_chats_per_round) == 0:
                        delay = random.randint(7200, 10800)
                        print(f"Waiting for {delay} seconds before the next round.")
                        await asyncio.sleep(delay)
                except httpx.RequestError:
                    print(f"Error occurred while sending request through proxy: {proxy}")


async def done_callback_command(callback_query: types.CallbackQuery):
    read = await sqlite_db.sql_read_as_list()
    res = [i for i in callback_query.data.replace('done ', '').split(',')]
    lel = [i for i in read if i[1] == res[0]]
    user_id = callback_query.from_user.id
    await auto_comment(user_id, lel)


async def random_sending(item: types.Message):
    if ID == item.from_user.id:
        read = await sqlite_db.sql_read_as_list()
        if len(read) == 0:
            await bot.send_message(item.from_user.id, text='upload something firstly')
        else:
            await auto_comment(item.from_user.id, read)
    else:
        await bot.send_message(item.from_user.id, text="U're not admin")


async def message_list(item: types.Message):
    if ID == item.from_user.id:
        await bot.send_message(item.from_user.id, 'Messages!')
        await sqlite_db.sql_read(item)
    else:
        await bot.send_message(item.from_user.id, text="U're not admin")


def reg_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(uploader, commands=['upload'], state=None)
    dp.register_message_handler(upload_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(input_name, content_types=['text'], state=FSMAdmin.name)
    dp.register_message_handler(cancel_state, commands=['cancel'], state="*")
    dp.register_message_handler(cancel_state, Text(equals='cancel', ignore_case=True), state='*')
    dp.register_message_handler(if_admin, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(delete_item, commands=['delete'], is_chat_admin=True)
    dp.register_message_handler(random_sending, commands=['random'])
    dp.register_message_handler(message_list, commands=['messagelist'])
    dp.register_callback_query_handler(del_callback_command, lambda x: x.data and x.data.startswith('del '))
    dp.register_callback_query_handler(done_callback_command, lambda x: x.data and x.data.startswith('done '))