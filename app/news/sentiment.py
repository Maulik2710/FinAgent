import pandas as pd

from transformers import pipeline

from app.data_pipeline.logger import logger
from app.news.config import SENTIMENT_MODEL


def load_sentiment_pipeline():
    """
    Load the FinBERT sentiment analysis pipeline.
    """

    logger.info("Loading FinBERT model...")

    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model=SENTIMENT_MODEL
    )

    return sentiment_pipeline


def analyze_sentiment(sentiment_pipeline, text: str) -> dict:
    """
    Analyze the sentiment of a single news article.
    """

    result = sentiment_pipeline(text)[0]

    return {
        "sentiment": result["label"],
        "confidence": result["score"],
    }


def analyze_news_dataframe(news_df: pd.DataFrame, sentiment_pipeline,) -> pd.DataFrame:
    """
    Analyze sentiment for all news articles.
    """

    news_df = news_df.copy()

    sentiments = []
    confidences = []

    for _, row in news_df.iterrows():

        title = row["title"]
        description = row["description"]

        text = (
            f"{title}. "
            f"{description if pd.notna(description) else ''}"
        )

        result = analyze_sentiment(
            sentiment_pipeline,
            text,
        )

        sentiments.append(result["sentiment"])
        confidences.append(result["confidence"])

    news_df["sentiment"] = sentiments
    news_df["confidence"] = confidences

    return news_df


def calculate_sentiment_score(news_df: pd.DataFrame,) -> float:
    """
    Calculate the average sentiment score.
    """

    sentiment_map = {
        "positive": 1,
        "neutral": 0,
        "negative": -1,
    }

    scores = news_df["sentiment"].str.lower().map(sentiment_map)

    return scores.mean()


# This is only for the Testing purpose
# if __name__ == "__main__":

#     from app.news.downloader import download_news

#     sentiment_pipeline = load_sentiment_pipeline()
#     news_df = download_news("AAPL")
#     news_df = analyze_news_dataframe(news_df,sentiment_pipeline,)
#     score = calculate_sentiment_score(news_df)
#     print(news_df)
#     print(f"\nOverall Sentiment Score: {score:.2f}")