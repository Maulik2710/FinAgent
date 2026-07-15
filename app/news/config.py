from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# News API
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

NEWS_BASE_URL = "https://newsapi.org/v2/everything"

# Number of articles to fetch
MAX_NEWS_ARTICLES = 10

# Hugging Face model
SENTIMENT_MODEL = "ProsusAI/finbert"

# Save downloaded news (optional)
NEWS_DIR = Path("data/news")
NEWS_DIR.mkdir(parents=True, exist_ok=True)

COMPANY_NAMES = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GOOGL": "Google",
    "AMZN": "Amazon",
    "META": "Meta",
    "TSLA": "Tesla",
    "NVDA": "NVIDIA",
    "AMD": "AMD",
    "NFLX": "Netflix",
    "JPM": "JPMorgan",
}

# Save the news
DATA_DIR = Path("data")

RAW_NEWS_DIR = NEWS_DIR / "raw"
SENTIMENT_NEWS_DIR = NEWS_DIR / "sentiment"

RAW_NEWS_DIR.mkdir(parents=True, exist_ok=True)
SENTIMENT_NEWS_DIR.mkdir(parents=True, exist_ok=True)