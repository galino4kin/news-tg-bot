from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Топ новостей')],
        [KeyboardButton(text='Суммаризация и сентимент анализ')],
        [KeyboardButton(text='Помощь')],
    ],
    resize_keyboard=True
)