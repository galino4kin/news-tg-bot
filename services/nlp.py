import requests
from openai import OpenAI
import re, os, json, time, logging
from dotenv import load_dotenv
from typing import Dict

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
        
    def summarize_text(self, text: str, max_tokens: int = 256) -> str:
        """Summarize the given text using OpenAI API"""
        prompt = f"""Imagine you are a journalist conducting research on the topic of {topic}. You have been given {n} articles to review. Produce a clear, informative summary that captures the key points without unnecessary detail:

                    {text}

                    Summary should be 1-3 sentences long. No personal opinions or commentary. Provide summary in the input language.
                    Do not put any additional phrases like "In summary" or "To conclude" at the beginning of the summary.
                    """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a journalist who performs a news analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.5,
            )
            
            summary = response.choices[0].message.content.strip()
            return summary
        except Exception as e:
            logger.error(f"Error during summarization: {e}")
            return "Error: Unable to summarize the text at this time."
        
    def sent_analysis(self, text: str) -> Dict:
        """Perform sentiment analysis on the given text using OpenAI API"""
        prompt = f"""Evaluate the sentiment expressed in the following text and classify it as Positive, Negative, or Neutral (Provide sentiment label in the input language):

                    {text}

                    Provide only one word as output: Positive, Negative, or Neutral."""
                    
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
            
            sentiment_raw = response.choices[0].message.content
            sentiment = sentiment_raw.split("$")[-1].strip()
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
        test_text = json.load(f)
    
    logger.info("Testing Summarization...")
    summary = nlp_service.summarize_text(test_text)
    logger.info(f"Summary: {summary}")
    
    logger.info("Testing Sentiment Analysis...")
    sentiment_result = nlp_service.sent_analysis(test_text)
    logger.info(f"Sentiment Analysis Result: {sentiment_result}")