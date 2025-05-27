from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



start_keyboard_reply = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Добавить заметку'),
     KeyboardButton(text='Удалить заметку'),
     KeyboardButton(text='Просмотреть все заметки')]
], resize_keyboard=True, one_time_keyboard=True)