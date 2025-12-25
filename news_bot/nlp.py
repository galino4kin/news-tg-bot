import requests
from openai import OpenAI
import os, json, logging
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NLPService:

    def __init__(self):
        OPENAI_APIKEY = os.getenv("OPENAI_APIKEY")
        self.client = OpenAI(api_key=OPENAI_APIKEY)

    @staticmethod
    def prepare_news_text(news: List[Dict], max_articles: int) -> str:
        """Aggregate descriptions of top news articles into a single text"""
        blocks = []

        for article in news[:max_articles]:
            desc = article.get("description")
            if desc:
                blocks.append(f"- {desc}")

        return "\n".join(blocks)

    def summarize_text(
        self,
        text: str,
        topic: str,
        n: int,
        max_tokens: int = 256) -> str:
        """Summarize aggregated top news using OpenAI API"""

        prompt = f"""
        You are analyzing {n} top news articles on the topic "{topic}".

        Produce a concise aggregated summary:
        - 2–4 sentences
        - neutral, factual tone
        - no opinions
        - no repetition
        - use the input language

        News summaries:
        {text}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a journalist who performs a news analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.4,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error during summarization: {e}")
            return "Error: Unable to summarize the text at this time."

    def sent_analysis(self, text: str) -> Dict:
        """Perform sentiment analysis on aggregated news text"""

        prompt = f"""
Evaluate the sentiment expressed in the following text.
Classify it as Positive, Negative, or Neutral.
Provide only one word as output.

{text}
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis expert."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=10,
                temperature=0.0,
            )

            sentiment = response.choices[0].message.content.strip()
            return {"sentiment": sentiment}

        except Exception as e:
            logger.error(f"Error during sentiment analysis: {e}")
            return {"error": "Unable to perform sentiment analysis at this time."}


if __name__ == "__main__":
    topic = "Python programming"
    n = 3

    nlp_service = NLPService()
    json_path = os.getenv("NEWS_JSON_PATH", "python_news.json")

    with open(json_path, "r", encoding="utf-8") as f:
        news = json.load(f)

    aggregated_text = nlp_service.prepare_news_text(news, max_articles=n)

    logger.info("Testing Summarization...")
    summary = nlp_service.summarize_text(
        text=aggregated_text,
        topic=topic,
        n=n
    )
    logger.info(f"Summary:\n{summary}")

    logger.info("Testing Sentiment Analysis...")
    sentiment_result = nlp_service.sent_analysis(aggregated_text)
    logger.info(f"Sentiment Analysis Result: {sentiment_result}")
