from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_keyboard_inline = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить заметку', callback_data='add')],
    [InlineKeyboardButton(text='Просмотреть все заметки', callback_data='show')],
    [InlineKeyboardButton(text='Удалить заметку', callback_data='delete')]
])

kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сок', callback_data='juice')],
    [InlineKeyboardButton(text='Чай', callback_data='tea')]
])