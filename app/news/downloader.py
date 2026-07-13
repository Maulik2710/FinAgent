import requests
import pandas as pd

from app.data_pipeline.logger import logger

from app.news.config import (
    NEWS_API_KEY,
    NEWS_BASE_URL,
    MAX_NEWS_ARTICLES,
    COMPANY_NAMES
)

def fetch_news(symbol: str) -> dict:
    """
    Fetch raw news data from NewsAPI.
    """

    logger.info(f"Downloading news for {symbol}...")

    params = {
         "q": COMPANY_NAMES.get(symbol, symbol),
        "apiKey": NEWS_API_KEY,
        "pageSize": MAX_NEWS_ARTICLES,
        "language": "en",
        "sortBy": "publishedAt",
    }

    response = requests.get(NEWS_BASE_URL,params=params,timeout=10,)

    response.raise_for_status()

    return response.json()

def extract_articles(news_data: dict) -> pd.DataFrame:
    """
    Extract useful information from NewsAPI response.
    """

    articles = news_data.get("articles", [])

    records = []

    for article in articles:

        records.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "source": article.get("source", {}).get("name"),
            "publishedAt": article.get("publishedAt"),
            "url": article.get("url"),
        })

    return pd.DataFrame(records)

def download_news(symbol: str) -> pd.DataFrame:
    """
    Download and prepare news articles for a stock.
    """

    news_data = fetch_news(symbol)

    news_df = extract_articles(news_data)

    logger.info(f"Downloaded {len(news_df)} articles for {symbol}.")

    return news_df

# This is only for the training purpose
if __name__ == "__main__":

    df = download_news("AAPL")

    print(df.head())