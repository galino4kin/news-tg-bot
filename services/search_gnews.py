import requests
import logging
import os
from typing import List, Dict
from dotenv import load_dotenv
import json

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class GNewsClient:
    """
    GNews Client

    Docs: https://gnews.io/docs/v4
    API key: https://gnews.io/
    Uses free tier
    """

    def __init__(self):
        self.api_key = os.getenv("GNEWS_API_KEY")
        self.base_url = "https://gnews.io/api/v4/search"

    def get_news(self, topic: str, max_results: int = 5) -> List[Dict]:
        """Get news by query topic using GNews"""
        if not self.api_key:
            logger.error("GNEWS_API_KEY not found in .env file")
            return []

        try:
            params = {
                "q": topic,
                "max": min(max_results, 10),
                "lang": "ru", #en/ru
                "sortby": "publishedAt",
                "apikey": self.api_key,
            }

            response = requests.get(self.base_url, params=params, timeout=15)

            if response.status_code == 200:
                data = response.json()
                articles = data.get("articles", [])

                news_list: List[Dict] = []
                for article in articles[:max_results]:
                    news_list.append({
                        "title": article.get("title", ""),
                        "description": article.get("description", ""),
                        "url": article.get("url", ""),
                        "published_at": article.get("publishedAt", ""),
                        "source": article.get("source", {}).get("name", ""),
                        "content": article.get("content", ""),
                    })

                logger.info(f"Found {len(news_list)} news articles for topic '{topic}'")
                return news_list

            elif response.status_code == 401:
                logger.error("Invalid GNews API key")
                return []
            elif response.status_code == 429:
                logger.warning("GNews rate limit exceeded")
                return []
            else:
                logger.error(f"GNews API error: {response.status_code}")
                return []

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during GNews request: {e}")
            return []

    def save_news(self, news: List[Dict], filename: str) -> None:
        """Save news articles to a JSON file"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(news, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(news)} articles to {filename}")


if __name__ == "__main__":
    logger.info("Testing GNews API...")
    client = GNewsClient()
