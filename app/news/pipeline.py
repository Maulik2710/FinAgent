import pandas as pd

from app.data_pipeline.logger import logger

from app.news.downloader import download_news, ARTICLE_COLUMNS
from app.news.sentiment import (
    load_sentiment_pipeline,
    analyze_news_dataframe,
    calculate_sentiment_score,
)
from app.news.storage import (
    save_raw_news,
    save_sentiment_news,
    load_sentiment_news,
    sentiment_news_exists,
    is_sentiment_stale,
)


class NoNewsFound(Exception):
    """NewsAPI worked, but returned no usable articles."""


def _fetch_and_analyze(symbol: str, sentiment_pipeline) -> pd.DataFrame:
    news_df = download_news(symbol)

    if news_df.empty:
        raise NoNewsFound(f"No news articles found for {symbol}.")

    save_raw_news(news_df, symbol)

    # Load FinBERT only now (not at all when cached news is used)
    if sentiment_pipeline is None:
        sentiment_pipeline = load_sentiment_pipeline()

    news_df = analyze_news_dataframe(news_df, sentiment_pipeline)

    save_sentiment_news(news_df, symbol)

    return news_df


def _build_result(news_df: pd.DataFrame, from_cache: bool) -> dict:
    score = calculate_sentiment_score(news_df)

    labels = (
        news_df["sentiment"].astype(str).str.lower()
        if "sentiment" in news_df.columns
        else pd.Series(dtype=str)
    )

    # NaN -> None so the frontend never shows "nan"
    records = news_df.astype(object).where(news_df.notna(), None).to_dict("records")

    return {
        "news": records,
        "score": score,
        "positive_count": int((labels == "positive").sum()),
        "neutral_count": int((labels == "neutral").sum()),
        "negative_count": int((labels == "negative").sum()),
        "from_cache": from_cache,
    }


def news_sentiment_pipeline(
    symbol: str,
    sentiment_pipeline=None,
    force_refresh: bool = False,
) -> dict:
    """
    Run the complete news sentiment analysis pipeline.

    - Saved results younger than NEWS_CACHE_HOURS are reused (no API call,
      no model loading).
    - If the download fails (rate limit, no internet), the last saved results
      are used instead of crashing.
    - If there are no articles and nothing saved, a neutral score (0.0) is returned.
    """
    symbol = symbol.upper()

    logger.info(f"Starting news sentiment analysis for {symbol}...")

    use_cache = (
        not force_refresh
        and sentiment_news_exists(symbol)
        and not is_sentiment_stale(symbol)
    )

    from_cache = False

    if use_cache:
        logger.info(f"Using cached news for {symbol}.")
        news_df = load_sentiment_news(symbol)
        from_cache = True

    else:
        try:
            news_df = _fetch_and_analyze(symbol, sentiment_pipeline)

        except NoNewsFound as e:
            if sentiment_news_exists(symbol):
                logger.warning(f"{e} Using last saved news.")
                news_df = load_sentiment_news(symbol)
                from_cache = True
            else:
                logger.warning(f"{e} Returning a neutral score.")
                news_df = analyze_news_dataframe(
                    pd.DataFrame(columns=ARTICLE_COLUMNS), None
                )

        except Exception as e:
            if sentiment_news_exists(symbol):
                logger.warning(f"News update failed for {symbol} ({e}). Using last saved news.")
                news_df = load_sentiment_news(symbol)
                from_cache = True
            else:
                raise

    result = _build_result(news_df, from_cache)

    logger.info(f"Overall sentiment score for {symbol}: {result['score']:.2f}")
    logger.info(f"News sentiment analysis completed for {symbol}.")

    return result


# This is only for testing purposes
if __name__ == "__main__":

    results = news_sentiment_pipeline("AAPL")

    print(f"\nScore: {results['score']:.2f}  (cached: {results['from_cache']})")
    print("Pipeline executed successfully.")