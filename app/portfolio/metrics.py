# This file is responsible for calculating financial metrics from historical stock prices.
import pandas as pd

from app.forecasting.dataset import load_processed_data
from app.portfolio.config import TRADING_DAYS

def load_close_prices(symbols: list[str]) -> pd.DataFrame:
    """
    Load the closing prices for multiple stocks.
    """

    close_prices = pd.DataFrame()

    for symbol in symbols:
        df = load_processed_data(symbol)

        close_prices[symbol] = df["Close"]

    return close_prices


def calculate_daily_returns(close_prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily percentage returns.
    """

    return close_prices.pct_change().dropna()


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


# Only Testing Purpose 
# if __name__ == "__main__":

#     from app.data_pipeline.config import STOCKS

#     prices = load_close_prices(STOCKS)
#     returns = calculate_daily_returns(prices)
#     annual_returns = calculate_annual_returns(returns)
#     covariance = calculate_covariance_matrix(returns)
#     print(prices.head())
#     print(returns.head())
#     print(annual_returns)
#     print(covariance)