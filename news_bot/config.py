import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

# Загрузка переменных окружения
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")

if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN не задан")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()