import time

import requests
import pandas as pd

from app.data_pipeline.logger import logger

from app.news.config import (
    NEWS_API_KEY,
    NEWS_BASE_URL,
    MAX_NEWS_ARTICLES,
    COMPANY_NAMES,
    COMPANY_SEARCH_TERMS,
    FINANCE_KEYWORDS,
    REQUEST_TIMEOUT,
    REQUEST_RETRIES,
    RETRY_DELAY_SECONDS,
)

ARTICLE_COLUMNS = ["title", "description", "source", "publishedAt", "url"]


def build_search_query(symbol: str) -> str:
    """
    Build a NewsAPI query such as:
    ("Apple" OR "AAPL") AND (stock OR shares OR earnings OR revenue OR investors)
    """
    terms = COMPANY_SEARCH_TERMS.get(symbol, [COMPANY_NAMES.get(symbol, symbol)])
    terms = list(dict.fromkeys(terms + [symbol]))   # remove duplicates, keep order

    names = " OR ".join(f'"{term}"' for term in terms)

    return f"({names}) AND ({FINANCE_KEYWORDS})"


def _safe_json(response: requests.Response) -> dict:
    try:
        return response.json()
    except ValueError:
        return {}


def fetch_news(symbol: str) -> dict:
    """
    Fetch raw news data from NewsAPI.

    The API key is sent in a header (not in the URL), so it can never leak
    into error messages, logs or the Streamlit error box.
    """
    if not NEWS_API_KEY:
        raise RuntimeError(
            "NEWS_API_KEY is not set. Add NEWS_API_KEY=your_key to your .env file."
        )

    logger.info(f"Downloading news for {symbol}...")

    params = {
        "q": build_search_query(symbol),
        "pageSize": MAX_NEWS_ARTICLES,
        "language": "en",
        "sortBy": "publishedAt",
        "searchIn": "title,description",
    }
    headers = {"X-Api-Key": NEWS_API_KEY}

    last_error = None

    for attempt in range(1, REQUEST_RETRIES + 1):
        try:
            response = requests.get(
                NEWS_BASE_URL,
                params=params,
                headers=headers,
                timeout=REQUEST_TIMEOUT,
            )
        except (requests.ConnectionError, requests.Timeout) as e:
            last_error = e
            logger.warning(f"{symbol}: network problem (attempt {attempt}): {e}")
            time.sleep(RETRY_DELAY_SECONDS)
            continue

        # Server-side problem: retry
        if response.status_code >= 500:
            last_error = RuntimeError(f"NewsAPI server error ({response.status_code}).")
            logger.warning(f"{symbol}: {last_error} (attempt {attempt})")
            time.sleep(RETRY_DELAY_SECONDS)
            continue

        data = _safe_json(response)

        # 401 bad key, 426/429 rate limit, 400 bad query ... -> do not retry
        if response.status_code != 200 or data.get("status") != "ok":
            message = data.get("message", response.reason)
            raise RuntimeError(f"NewsAPI error ({response.status_code}): {message}")

        return data

    raise RuntimeError(
        f"Could not reach NewsAPI after {REQUEST_RETRIES} attempts: {last_error}"
    )


def extract_articles(news_data: dict) -> pd.DataFrame:
    """
    Extract useful information from the NewsAPI response.
    Removed / empty / duplicate articles are dropped.
    """
    records = []

    for article in news_data.get("articles", []):

        title = article.get("title")

        # NewsAPI returns "[Removed]" for articles that were taken down
        if not title or title.strip() == "[Removed]":
            continue

        description = article.get("description")
        if description and description.strip() == "[Removed]":
            description = None

        records.append({
            "title": title.strip(),
            "description": description,
            "source": (article.get("source") or {}).get("name"),
            "publishedAt": article.get("publishedAt"),
            "url": article.get("url"),
        })

    df = pd.DataFrame(records, columns=ARTICLE_COLUMNS)

    if df.empty:
        return df

    df = df.drop_duplicates(subset="url").drop_duplicates(subset="title")
    df = df.sort_values("publishedAt", ascending=False).reset_index(drop=True)

    return df


def download_news(symbol: str) -> pd.DataFrame:
    """
    Download and prepare news articles for a stock.
    """
    news_data = fetch_news(symbol)

    news_df = extract_articles(news_data)

    logger.info(f"Downloaded {len(news_df)} articles for {symbol}.")

    return news_df


# This is only for testing purposes
if __name__ == "__main__":

    df = download_news("AAPL")

    print(df.head())