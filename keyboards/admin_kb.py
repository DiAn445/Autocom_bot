from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

upload_bt = KeyboardButton('/upload')
cancel_bt = KeyboardButton('/cancel')
random_bt = KeyboardButton('/random')
message_bt = KeyboardButton('/messagelist')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).row(upload_bt, cancel_bt).row(random_bt, message_bt)
