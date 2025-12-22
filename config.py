import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
NEWS_API_KEY = os.environ["NEWS_API_KEY"]
GOOGLE_CSE_ID = os.environ["GOOGLE_CSE_ID"]

SEARCH_TOP_K = 5
SUMMARY_MAX_TOKENS = 256