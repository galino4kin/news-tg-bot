import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from search_gnews import GNewsClient
import json
from nlp import NLPService
import logging 

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Переменные для отслеживания состояния тем и опций
current_topic = None
pending_action = None 

# Инициализация бота
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN не задан")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Создание экземпляров классов
gnews_client = GNewsClient()
nlp_service = NLPService()

# Клавиатуры
keyboard_main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Топ новостей')],
        [KeyboardButton(text='Суммаризация и сентимент анализ')],
        [KeyboardButton(text='Помощь')],
    ],
    resize_keyboard=True
)

# Команды
@dp.message(Command('start'))
async def start_command(message: types.Message):
    await message.answer( 'Привет, я — бот-аналитик новостей. Отправь мне тему, и я:\n\n'
                          '🔍 Найду топ новостей по теме\n'
                          '📝 Сделаю краткую выжимку\n' 
                          '📊 Проанализирую тон\n'
                          'Выберите действие:',
                            reply_markup=keyboard_main)

@dp.message(Command('help'))
@dp.message(F.text == 'Помощь')
async def help_command(message: types.Message):
    await message.answer( 'Доступные команды:\n\n' 
                        '/start — приветствие\n' 
                        '/help — помощь\n' 
                        '/top_news — топ новостей\n' 
                        '/extra — суммаризация и анализ тональности новостей\n\n'
                        'Бот умеет искать новости на различные темы. Достаточно просто написать интересующий топик на русском языке. После этого вы сможете получить топ-новостей со ссылками на источники или их краткую выжимку с анализом тональности.\n\n' 
                        'Попробуйте переформулировать тему, если бот не найдет то, что вы ищете')

# Опции
@dp.message(Command('top_news'))
@dp.message(F.text == 'Топ новостей')
async def top_news_request(message: types.Message):
    global pending_action, current_topic
    pending_action = "top_news"
    current_topic = None
    await message.answer("Введите тему для поиска новостей:")

@dp.message(Command('extra'))
@dp.message(F.text == 'Суммаризация и сентимент анализ')
async def extra_request(message: types.Message):
    global pending_action, current_topic
    pending_action = "extra"
    current_topic = None
    await message.answer("Введите тему для суммаризации и сентимент анализа:")

# Обработка текстовых сообщений
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
        await show_top_news(message)
    elif pending_action == "extra":
        await show_summary_sentiment(message)

    # Сброс темы и опции
    pending_action = None
    current_topic = None

# Функции
async def show_top_news(message: types.Message):
    await message.answer(f"🔍 Ищу новости по теме: «{current_topic}»")
    try:
        news = gnews_client.get_news(current_topic, max_results=5)
        if not news:
            await message.answer("Новости не найдены.")
            return

        response = f"Топ новостей по теме «{current_topic}»:\n\n"
        for i, article in enumerate(news, 1):
            response += (
                f"{i}. {article.get('title', 'Без заголовка')}\n"
                f"{article.get('url', '')}\n\n"
            )

        await message.answer(response, disable_web_page_preview=True)

    except Exception:
        logger.exception("Ошибка при получении новостей")
        await message.answer("Ошибка при получении новостей.")

async def show_summary_sentiment(message: types.Message):
    await message.answer(f"📝 Анализирую тему: «{current_topic}»")
    try:
        news = gnews_client.get_news(current_topic, max_results=5)
        if not news:
            await message.answer("Недостаточно данных")
            return

        text = nlp_service.prepare_news_text(news, max_articles=3)
        summary = nlp_service.summarize_text(
            text=text,
            topic=current_topic,
            n=3,
            max_tokens=200
        )

        sentiment = nlp_service.sent_analysis(text).get("sentiment", "Не определён")

        await message.answer(
            f"Краткая выжимка:\n{summary}\n\n"
            f"Тональность: {sentiment}"
        )

    except Exception:
        logger.exception("Ошибка анализа")
        await message.answer("Ошибка при анализе новостей.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
