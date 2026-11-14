from functools import lru_cache

import pandas as pd

from transformers import pipeline

from app.data_pipeline.logger import logger
from app.news.config import (
    SENTIMENT_MODEL,
    SENTIMENT_BATCH_SIZE,
    MAX_TEXT_TOKENS,
)

SENTIMENT_MAP = {
    "positive": 1,
    "neutral": 0,
    "negative": -1,
}


@lru_cache(maxsize=1)
def load_sentiment_pipeline():
    """
    Load the FinBERT sentiment analysis pipeline.

    Cached: the (large) model is loaded only once per Python process, no
    matter how many times the news / recommendation pipelines are called.
    """
    logger.info("Loading FinBERT model...")

    return pipeline(
        "sentiment-analysis",
        model=SENTIMENT_MODEL,
    )


def build_article_text(title, description) -> str:
    """
    Combine title and description into one text for the model.
    """
    title = title if pd.notna(title) else ""
    description = description if pd.notna(description) else ""

    return f"{title}. {description}".strip()


def analyze_sentiment(sentiment_pipeline, text: str) -> dict:
    """
    Analyze the sentiment of a single piece of text.
    """
    result = sentiment_pipeline(
        text,
        truncation=True,
        max_length=MAX_TEXT_TOKENS,
    )[0]

    return {
        "sentiment": result["label"],
        "confidence": result["score"],
    }


def analyze_news_dataframe(news_df: pd.DataFrame, sentiment_pipeline) -> pd.DataFrame:
    """
    Analyze sentiment for all news articles (batched, long texts truncated
    to FinBERT's 512-token limit).
    """
    news_df = news_df.copy()

    if news_df.empty:
        news_df["sentiment"] = pd.Series(dtype=object)
        news_df["confidence"] = pd.Series(dtype=float)
        return news_df

    texts = [
        build_article_text(row["title"], row.get("description"))
        for _, row in news_df.iterrows()
    ]

    results = sentiment_pipeline(
        texts,
        batch_size=SENTIMENT_BATCH_SIZE,
        truncation=True,
        max_length=MAX_TEXT_TOKENS,
    )

    news_df["sentiment"] = [r["label"].lower() for r in results]
    news_df["confidence"] = [float(r["score"]) for r in results]

    return news_df


def calculate_sentiment_score(news_df: pd.DataFrame) -> float:
    """
    Average sentiment score in [-1, 1]
    (positive = +1, neutral = 0, negative = -1). Returns 0.0 if there is no news.
    """
    if news_df.empty or "sentiment" not in news_df.columns:
        return 0.0

    scores = news_df["sentiment"].astype(str).str.lower().map(SENTIMENT_MAP)

    score = scores.mean()

    return 0.0 if pd.isna(score) else float(score)


# This is only for testing purposes
if __name__ == "__main__":

    from app.news.storage import load_raw_news

    sentiment_pipeline = load_sentiment_pipeline()
    news_df = load_raw_news("AAPL")
    news_df = analyze_news_dataframe(news_df, sentiment_pipeline)
    score = calculate_sentiment_score(news_df)
    print(news_df)
    print(f"\nOverall Sentiment Score: {score:.2f}")