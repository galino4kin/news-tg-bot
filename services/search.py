import requests
import logging
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv
import json

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewsAPIClient:
    """
    NewsAPI Client
    
    Docs: https://newsapi.org/docs
    API key: https://newsapi.org/register
    Uses free tier (100 call per day)
    """
    
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"
    
    def get_news(self, topic: str, max_results: int = 5) -> List[Dict]:
        """Get news by query topic"""
        if not self.api_key:
            logger.error("NEWS_API_KEY not found in .env file")
            return []
        
        try:
            params = {
                'q': topic,
                'pageSize': min(max_results, 10),
                'apiKey': self.api_key,
                'language': 'ru', # en/ru
                'sortBy': 'publishedAt'
            }
            
            response = requests.get(self.base_url, params=params, timeout=15)
            if response.status_code == 200:
            
            # If 200:
                data = response.json()
                articles = data.get('articles', [])
                
                news_list = []
                for article in articles[:max_results]:
                    news_list.append({
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'url': article.get('url', ''),
                        'published_at': article.get('publishedAt', ''),
                        'source': article.get('source', {}).get('name', ''),
                        'content': article.get('content', ''),
                    })
                
                logger.info(f"Found {len(news_list)} news articles for topic '{topic}'")
                return news_list
                
            elif response.status_code == 401:
                logger.error("Invalid NewsAPI key")
                return []
            elif response.status_code == 429:
                logger.warning("NewsAPI rate limit exceeded")
                return []
            else:
                logger.error(f"NewsAPI error: {response.status_code}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error during news request: {e}")
            return []
    def save_news(self, news: List[Dict], filename: str) -> None:
        """Save news articles to a JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(news, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(news)} articles to {filename}")

if __name__ == "__main__":    
    logger.info("Testing News API...")
    news = NewsAPIClient()
    if news.api_key:
        python_news = news.get_news("программирование", max_results=3)
        news.save_news(python_news, "python_news.json")
        for article in python_news:
            logger.info(f"News: {article['title']}")
    else:
        logger.warning("NewsAPI key not configured")
        pass
    