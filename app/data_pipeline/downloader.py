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
    AUTO_ADJUST
)
def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize column names returned by external data sources.
    """
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    return df

def download_stock(symbol: str) -> pd.DataFrame:
    """
    Download historical stock data for a single stock.
    """
    logger.info(f"Downloading {symbol}...")
       
    try:

        df = yf.download(
            symbol,
            start=START_DATE,
            end=END_DATE,
            interval=INTERVAL,
            auto_adjust=AUTO_ADJUST,
            progress=False
        )

        df = normalize_columns(df)

        return df
    except Exception as e:

        logger.error(f"Failed to download {symbol}: {e}")

        return pd.DataFrame()

def save_stock(df: pd.DataFrame, symbol: str) -> None:
    """
    Save stock data as CSV.
    """
    file_path = RAW_DATA_DIR / f"{symbol}.csv"
    df.to_csv(file_path)
    logger.info(f"{symbol} saved successfully.")

def download_all_stocks() -> None:

    for symbol in STOCKS:
        df = download_stock(symbol)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        print(df.head())
        print(df.columns)
        try:
            validate_dataframe(df)
            df = clean_stock_data(df)
            validate_dataframe(df)
            save_stock(df, symbol)
        except ValueError as e:
            logger.error(f"{symbol}: {e}")
            continue
        
if __name__ == "__main__":
    logger.info("Starting stock data download...")
    download_all_stocks()
    logger.info("All downloads completed.")