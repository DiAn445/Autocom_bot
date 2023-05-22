from aiogram import types, Dispatcher
from BotCreator import bot
from keyboards.common_kb import client_keyboard

redirection = """<b><i>U can communicate with bot only in private messages
                 Please, text him</i></b>\n
                 <b>https://t.me/user_send_bot</b>
                 """


async def command_start(answer: types.Message):
    try:
        await bot.send_message(answer.from_user.id, f'Greetings! chat_id={answer.chat.id}', reply_markup=client_keyboard)
        await answer.delete()
    except:
        await answer.reply(redirection)


def reg_handlers(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])