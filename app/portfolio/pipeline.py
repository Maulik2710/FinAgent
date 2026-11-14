import numpy as np

from app.data_pipeline.logger import logger
from app.data_pipeline.config import STOCKS, PROCESSED_DATA_DIR

from app.portfolio.metrics import (
    load_close_prices,
    calculate_daily_returns,
    calculate_annual_returns,
    calculate_covariance_matrix,
)

from app.portfolio.optimizer import optimize_portfolio
from app.portfolio.risk import calculate_portfolio_summary

# Remembers the last result; reused while the processed data files are unchanged
_cache = {"signature": None, "result": None}


def _signature(symbols: list) -> tuple:
    """Fingerprint of the processed files the result depends on."""
    parts = []
    for symbol in symbols:
        path = PROCESSED_DATA_DIR / f"{symbol}.csv"
        parts.append((symbol, path.stat().st_mtime_ns if path.exists() else None))
    return tuple(parts)


def _copy(result: dict) -> dict:
    """Return a copy, so callers can never modify the cached result."""
    copied = dict(result)
    copied["weights"] = result["weights"].copy()
    copied["weights_by_symbol"] = dict(result["weights_by_symbol"])
    copied["benchmark"] = dict(result["benchmark"])
    return copied


def portfolio_optimization_pipeline(symbols: list = None, force_refresh: bool = False) -> dict:
    """
    Run the complete portfolio optimization pipeline.

    Returns a dict with:
      symbols, weights (numpy array, same order as symbols), return,
      volatility, sharpe, success,
      weights_by_symbol  : {"AAPL": 0.12, ...}   (easier lookups)
      benchmark          : equal-weight portfolio return / volatility / sharpe
      period, observations : the data window the numbers are based on
    """
    symbols = list(symbols) if symbols else list(STOCKS)

    signature = _signature(symbols)

    if (
        not force_refresh
        and _cache["result"] is not None
        and _cache["signature"] == signature
    ):
        logger.info("Using cached portfolio optimization.")
        return _copy(_cache["result"])

    logger.info("Starting portfolio optimization...")

    prices = load_close_prices(symbols)
    daily_returns = calculate_daily_returns(prices)
    annual_returns = calculate_annual_returns(daily_returns)
    covariance_matrix = calculate_covariance_matrix(daily_returns)

    # Use the column order of the price table, so weights always match symbols
    symbols = list(prices.columns)

    result = optimize_portfolio(
        annual_returns.values,
        covariance_matrix.values,
        symbols=symbols,
    )

    equal_weights = np.ones(len(symbols)) / len(symbols)
    benchmark = calculate_portfolio_summary(
        equal_weights, annual_returns.values, covariance_matrix.values
    )

    result["weights_by_symbol"] = {
        symbol: float(weight) for symbol, weight in zip(symbols, result["weights"])
    }
    result["benchmark"] = benchmark
    result["period"] = (str(prices.index[0].date()), str(prices.index[-1].date()))
    result["observations"] = len(daily_returns)

    _cache["signature"] = signature
    _cache["result"] = result

    logger.info("Portfolio optimization completed successfully.")

    return _copy(result)


# This is only for testing purposes.
if __name__ == "__main__":

    from app.portfolio.optimizer import display_allocation

    result = portfolio_optimization_pipeline()
    display_allocation(result)
    print(f"\nData: {result['period'][0]} to {result['period'][1]} "
          f"({result['observations']} daily returns)")