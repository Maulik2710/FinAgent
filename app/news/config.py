import os
from dotenv import load_dotenv

from app.data_pipeline.config import PROJECT_ROOT, NEWS_DATA_DIR

# Load the .env file (project root first, then the app/ folder, then default lookup)
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(PROJECT_ROOT / "app" / ".env")
load_dotenv()

# ----------------------------
# News API
# ----------------------------

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

NEWS_BASE_URL = "https://newsapi.org/v2/everything"

# Number of articles to fetch per stock (one API request per stock).
# NewsAPI free plan: 100 requests/day, so keep this to ONE request per refresh.
MAX_NEWS_ARTICLES = 20

REQUEST_TIMEOUT = 10        # seconds
REQUEST_RETRIES = 3
RETRY_DELAY_SECONDS = 2

# Reuse saved news/sentiment for this many hours before calling the API again
NEWS_CACHE_HOURS = 6

# ----------------------------
# Sentiment model
# ----------------------------

SENTIMENT_MODEL = "ProsusAI/finbert"
SENTIMENT_BATCH_SIZE = 8
MAX_TEXT_TOKENS = 512       # FinBERT's input limit

# ----------------------------
# Companies
# ----------------------------

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

# Search terms per stock. "Apple" or "Amazon" alone also match fruit and
# rainforest articles, so every query is combined with finance keywords.
COMPANY_SEARCH_TERMS = {
    "AAPL": ["Apple"],
    "MSFT": ["Microsoft"],
    "GOOGL": ["Google", "Alphabet"],
    "AMZN": ["Amazon"],
    "META": ["Meta Platforms", "Facebook"],
    "TSLA": ["Tesla"],
    "NVDA": ["NVIDIA"],
    "AMD": ["AMD", "Advanced Micro Devices"],
    "NFLX": ["Netflix"],
    "JPM": ["JPMorgan", "JPMorgan Chase"],
}

FINANCE_KEYWORDS = "stock OR shares OR earnings OR revenue OR investors"

# ----------------------------
# Storage (absolute paths, same data/news folder as the data pipeline)
# ----------------------------

NEWS_DIR = NEWS_DATA_DIR

RAW_NEWS_DIR = NEWS_DIR / "raw"
SENTIMENT_NEWS_DIR = NEWS_DIR / "sentiment"

RAW_NEWS_DIR.mkdir(parents=True, exist_ok=True)
SENTIMENT_NEWS_DIR.mkdir(parents=True, exist_ok=True)