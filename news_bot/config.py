import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

# Загрузка переменных окружения
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN не задан")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()