import asyncio
from aiogram import types, F
from aiogram.filters import Command

from news_bot.config import bot, dp
from news_bot.states import current_topic, pending_action
from news_bot.services import gnews_client, nlp_service
from news_bot.keyboards import keyboard_main
from news_bot.handlers import start_command, help_command
from news_bot.news_functions import show_top_news, show_summary_sentiment

@dp.message(Command('start'))
async def start_handler(message: types.Message):
    await start_command(message, keyboard_main)

@dp.message(Command('help'))
@dp.message(F.text == 'Помощь')
async def help_handler(message: types.Message):
    await help_command(message)

@dp.message(Command('top_news'))
@dp.message(F.text == 'Топ новостей')
async def top_news_handler(message: types.Message):
    global pending_action, current_topic
    pending_action = "top_news"
    current_topic = None
    await message.answer("Введите тему для поиска новостей:")

@dp.message(Command('extra'))
@dp.message(F.text == 'Суммаризация и сентимент анализ')
async def extra_handler(message: types.Message):
    global pending_action, current_topic
    pending_action = "extra"
    current_topic = None
    await message.answer("Введите тему для суммаризации и сентимент анализа:")

@dp.message()
async def handle_text(message: types.Message):
    global current_topic, pending_action

    text = message.text.strip()

    # Если действие не выбрано
    if not pending_action:
        await message.answer(
            "Сначала выберите действие:",
            reply_markup=keyboard_main
        )
        return

    # Проверка длины темы
    if len(text) < 2:
        await message.answer("Тема слишком короткая. Попробуйте снова")
        return

    current_topic = text

    if pending_action == "top_news":
        await show_top_news(message, current_topic, gnews_client)
    elif pending_action == "extra":
        await show_summary_sentiment(message, current_topic, gnews_client, nlp_service)

    # Сброс темы и опции
    pending_action = None
    current_topic = None

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())