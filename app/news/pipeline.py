from app.data_pipeline.logger import logger

from app.news.downloader import download_news
from app.news.sentiment import (
    load_sentiment_pipeline,
    analyze_news_dataframe,
    calculate_sentiment_score,
)
from app.news.storage import save_raw_news, save_sentiment_news

def news_sentiment_pipeline(symbol: str, sentiment_pipeline=None,) -> dict:
    """
    Run the complete news sentiment analysis pipeline.
    """

    logger.info(f"Starting news sentiment analysis for {symbol}...")

    # Load FinBERT only if it hasn't been provided
    if sentiment_pipeline is None:
        sentiment_pipeline = load_sentiment_pipeline()

    # Download latest news
    news_df = download_news(symbol)
    
    # Save the Downloaded news
    save_raw_news(news_df, symbol)

    # Analyze sentiment
    news_df = analyze_news_dataframe(news_df, sentiment_pipeline,)
    
    # Save the Downloaded news with sentiment
    save_sentiment_news(news_df, symbol)

    # Calculate overall sentiment score
    sentiment_score = calculate_sentiment_score(news_df)

    logger.info(f"Overall sentiment score for {symbol}: {sentiment_score:.2f}")

    # print("\nNews Sentiment Results\n")
    # print(news_df)

    # print("\nOverall Sentiment Score")
    # print("-----------------------")
    # print(f"{sentiment_score:.2f}")

    logger.info(f"News sentiment analysis completed for {symbol}.")

    return {
        "news": news_df.to_dict("records"),
        "score": sentiment_score,
    }

# This is only for the Testing Purpose
if __name__ == "__main__":

    results = news_sentiment_pipeline("AAPL")

    print("\nPipeline executed successfully.")