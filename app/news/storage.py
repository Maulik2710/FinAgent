from pathlib import Path
import pandas as pd

from app.data_pipeline.logger import logger
from app.news.config import (
    RAW_NEWS_DIR,
    SENTIMENT_NEWS_DIR,
)

from datetime import datetime


def save_raw_news(news_df: pd.DataFrame, symbol: str) -> None:
    """
    Save downloaded news articles.
    """

    file_path = RAW_NEWS_DIR / f"{symbol}.csv"
    news_df.to_csv(file_path, index=False)
    logger.info(f"Raw news saved for {symbol}.")


def load_raw_news(symbol: str) -> pd.DataFrame:
    """
    Load previously downloaded news.
    """

    file_path = RAW_NEWS_DIR / f"{symbol}.csv"
    if not file_path.exists():
        raise FileNotFoundError(
            f"No raw news found for {symbol}."
        )
    logger.info(f"Loading raw news for {symbol}.")

    return pd.read_csv(file_path)


def save_sentiment_news(news_df: pd.DataFrame, symbol: str) -> None:
    """
    Save news with sentiment labels.
    """

    file_path = SENTIMENT_NEWS_DIR / f"{symbol}.csv"
    news_df.to_csv(file_path, index=False)
    logger.info(f"Sentiment news saved for {symbol}.")


def load_sentiment_news(symbol: str) -> pd.DataFrame:
    """
    Load sentiment analyzed news.
    """

    file_path = SENTIMENT_NEWS_DIR / f"{symbol}.csv"
    if not file_path.exists():
        raise FileNotFoundError(
            f"No sentiment news found for {symbol}."
        )
    logger.info(f"Loading sentiment news for {symbol}.")

    return pd.read_csv(file_path)


def raw_news_exists(symbol: str) -> bool:
    """
    Check whether raw news exists.
    """

    return (RAW_NEWS_DIR / f"{symbol}.csv").exists()


def sentiment_news_exists(symbol: str) -> bool:
    """
    Check whether sentiment news exists.
    """

    return (SENTIMENT_NEWS_DIR / f"{symbol}.csv").exists()


def is_news_stale(symbol: str, hours: int = 6) -> bool:
    """
    Check whether cached raw news is older than the specified number of hours.
    """

    file_path = RAW_NEWS_DIR / f"{symbol}.csv"

    if not file_path.exists():
        return True

    modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)

    elapsed_hours = (
        datetime.now() - modified_time
    ).total_seconds() / 3600

    return elapsed_hours >= hours

if __name__ == "__main__":

    raw = load_raw_news("AAPL")
    print(raw.head())

    sentiment = load_sentiment_news("AAPL")
    print(sentiment.head())