from app.data_pipeline.logger import logger
from app.data_pipeline.config import STOCKS
from app.portfolio.metrics import (
    load_close_prices,
    calculate_daily_returns,
    calculate_annual_returns,
    calculate_covariance_matrix,
)

from app.portfolio.optimizer import (
    optimize_portfolio,
    display_allocation,
)


def portfolio_optimization_pipeline() -> dict:
    """
    Run the complete portfolio optimization pipeline.
    """

    logger.info("Starting portfolio optimization...")

    logger.info("Loading stock prices...")
    prices = load_close_prices(STOCKS)

    logger.info("Calculating daily returns...")
    daily_returns = calculate_daily_returns(prices)

    logger.info("Calculating annual returns...")
    annual_returns = calculate_annual_returns(daily_returns)

    logger.info("Calculating covariance matrix...")
    covariance_matrix = calculate_covariance_matrix(daily_returns)

    logger.info("Optimizing portfolio...")
    result = optimize_portfolio(annual_returns.values, covariance_matrix.values,)

    display_allocation(result)

    logger.info("Portfolio optimization completed successfully.")

    return result


if __name__ == "__main__":

    portfolio_optimization_pipeline()