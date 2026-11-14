# This file is responsible for calculating financial metrics from historical stock prices.
import pandas as pd

from app.data_pipeline.config import PROCESSED_DATA_DIR
from app.data_pipeline.logger import logger
from app.portfolio.config import TRADING_DAYS, LOOKBACK_DAYS, MIN_OBSERVATIONS


def load_close_prices(symbols: list, lookback_days=LOOKBACK_DAYS) -> pd.DataFrame:
    """
    Load the closing prices for multiple stocks, aligned BY DATE.

    (Aligning by row number would pair different calendar days across stocks
    whenever their histories start on different dates, which corrupts the
    covariance matrix.) Only days where every stock has a price are kept.
    """
    series = {}

    for symbol in symbols:

        file_path = PROCESSED_DATA_DIR / f"{symbol}.csv"

        if not file_path.exists():
            raise FileNotFoundError(
                f"Processed data for {symbol} not found. "
                "Run the downloader and the feature engineering pipeline first."
            )

        df = pd.read_csv(file_path, usecols=["Date", "Close"], parse_dates=["Date"])

        df = df.drop_duplicates(subset="Date").set_index("Date").sort_index()

        series[symbol] = df["Close"]

    prices = pd.concat(series, axis=1).dropna()

    if len(prices) < MIN_OBSERVATIONS:
        raise ValueError(
            f"Only {len(prices)} common trading days across {len(symbols)} stocks "
            f"(need at least {MIN_OBSERVATIONS})."
        )

    if lookback_days:
        # +1 because N prices give N-1 returns
        prices = prices.tail(lookback_days + 1)

    logger.info(
        f"Loaded {len(prices)} aligned prices "
        f"({prices.index[0].date()} to {prices.index[-1].date()})."
    )

    return prices


def calculate_daily_returns(close_prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily percentage returns.
    """
    return close_prices.pct_change(fill_method=None).dropna()


def calculate_annual_returns(daily_returns: pd.DataFrame) -> pd.Series:
    """
    Calculate expected annual return.
    """
    return daily_returns.mean() * TRADING_DAYS


def calculate_covariance_matrix(daily_returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate annualized covariance matrix.
    """
    return daily_returns.cov() * TRADING_DAYS


# Only for testing purposes
if __name__ == "__main__":

    from app.data_pipeline.config import STOCKS

    prices = load_close_prices(STOCKS)
    returns = calculate_daily_returns(prices)
    annual_returns = calculate_annual_returns(returns)
    covariance = calculate_covariance_matrix(returns)
    print(prices.head())
    print(returns.head())
    print(annual_returns)
    print(covariance)