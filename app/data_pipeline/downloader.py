import time

import yfinance as yf
import pandas as pd

from .logger import logger
from .validator import validate_dataframe
from .cleaner import clean_stock_data
from .config import (
    RAW_DATA_DIR,
    STOCKS,
    START_DATE,
    END_DATE,
    INTERVAL,
    AUTO_ADJUST,
    DOWNLOAD_RETRIES,
    RETRY_DELAY_SECONDS,
)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names returned by external data sources.
    (Newer yfinance versions return a MultiIndex: (Price, Ticker).)
    """
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    return df


def download_stock(symbol: str) -> pd.DataFrame:
    """
    Download historical stock data for a single stock, with retries.
    Returns an empty dataframe if every attempt fails.
    """
    for attempt in range(1, DOWNLOAD_RETRIES + 1):
        logger.info(f"Downloading {symbol} (attempt {attempt}/{DOWNLOAD_RETRIES})...")

        try:
            df = yf.download(
                symbol,
                start=START_DATE,
                end=END_DATE,
                interval=INTERVAL,
                auto_adjust=AUTO_ADJUST,
                progress=False,
            )

            df = normalize_columns(df)

            if not df.empty:
                return df

            logger.warning(f"{symbol}: download returned no data.")

        except Exception as e:
            logger.error(f"Failed to download {symbol}: {e}")

        if attempt < DOWNLOAD_RETRIES:
            time.sleep(RETRY_DELAY_SECONDS)

    return pd.DataFrame()


def save_stock(df: pd.DataFrame, symbol: str) -> None:
    """
    Save stock data as CSV (the index is saved as the "Date" column).
    """
    file_path = RAW_DATA_DIR / f"{symbol}.csv"
    df.to_csv(file_path)
    logger.info(f"{symbol} saved successfully ({len(df)} rows).")


def download_all_stocks() -> dict:
    """
    Download, validate, clean and save every stock in STOCKS.
    Returns {"success": [...], "failed": [...]}.
    """
    success, failed = [], []

    for symbol in STOCKS:
        df = download_stock(symbol)

        try:
            validate_dataframe(df)                  # structure check
            df = clean_stock_data(df)
            validate_dataframe(df, strict=True)     # clean-data check
            save_stock(df, symbol)
            success.append(symbol)

        except ValueError as e:
            logger.error(f"{symbol}: {e}")
            failed.append(symbol)

    logger.info(f"Downloaded: {success}")
    if failed:
        logger.warning(f"Failed: {failed}")

    return {"success": success, "failed": failed}


if __name__ == "__main__":
    logger.info("Starting stock data download...")
    download_all_stocks()
    logger.info("All downloads completed.")