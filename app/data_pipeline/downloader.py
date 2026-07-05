import yfinance as yf
import pandas as pd

from .logger import logger
from .config import (
    RAW_DATA_DIR,
    STOCKS,
    START_DATE,
    END_DATE,
    INTERVAL,
    AUTO_ADJUST
)

def download_stocks(symbols: str) -> pd.DataFrame:
    pass

def save_stock(df: pd.DataFrame, symbol: str):
    pass
