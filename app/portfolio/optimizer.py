import numpy as np
from scipy.optimize import minimize

from app.data_pipeline.config import STOCKS

from app.portfolio.metrics import (
    load_close_prices,
    calculate_daily_returns,
    calculate_annual_returns,
    calculate_covariance_matrix,
)

from app.portfolio.risk import (
    calculate_portfolio_return,
    calculate_portfolio_volatility,
    calculate_sharpe_ratio,
)


def negative_sharpe_ratio(weights: np.ndarray, annual_returns: np.ndarray, covariance_matrix: np.ndarray,) -> float:
    """
    Objective function for optimization.
    Returns the negative Sharpe Ratio because scipy minimizes.
    """

    portfolio_return = calculate_portfolio_return(weights, annual_returns)

    portfolio_volatility = calculate_portfolio_volatility(weights, covariance_matrix)

    sharpe_ratio = calculate_sharpe_ratio(portfolio_return, portfolio_volatility)

    return -sharpe_ratio


def optimize_portfolio(annual_returns: np.ndarray, covariance_matrix: np.ndarray,) -> dict:
    """
    Find the portfolio allocation that maximizes the Sharpe Ratio.
    """

    number_of_stocks = len(annual_returns)

    initial_weights = np.ones(number_of_stocks) / number_of_stocks

    constraints = (
        {
            "type": "eq",
            "fun": lambda weights: np.sum(weights) - 1,
        },
    )

    bounds = tuple(
        (0, 1)
        for _ in range(number_of_stocks)
    )

    result = minimize(
        fun=negative_sharpe_ratio,
        x0=initial_weights,
        args=(
            annual_returns,
            covariance_matrix,
        ),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )

    weights = result.x

    portfolio_return = calculate_portfolio_return(weights, annual_returns,)

    portfolio_volatility = calculate_portfolio_volatility(weights, covariance_matrix,)

    sharpe_ratio = calculate_sharpe_ratio(portfolio_return, portfolio_volatility,)

    return {
        "weights": weights,
        "return": portfolio_return,
        "volatility": portfolio_volatility,
        "sharpe": sharpe_ratio,
    }


def display_allocation(result: dict) -> None:
    """
    Display the optimized portfolio allocation and statistics.
    """

    print("\nRecommended Portfolio Allocation\n")
    
    allocations = sorted(
        zip(STOCKS, result["weights"]),
        key=lambda x: x[1],
        reverse=True
    )

    for stock, weight in allocations:
        print(f"{stock:<6}: {weight * 100:.2f}%")

    print("\nPortfolio Statistics")
    print("-" * 30)
    print(f"Expected Return : {result['return']:.2%}")
    print(f"Volatility      : {result['volatility']:.2%}")
    print(f"Sharpe Ratio    : {result['sharpe']:.4f}")


# This is Only for the training Purpose
if __name__ == "__main__":

    prices = load_close_prices(STOCKS)
    daily_returns = calculate_daily_returns(prices)
    annual_returns = calculate_annual_returns(daily_returns)
    covariance_matrix = calculate_covariance_matrix(daily_returns)
    result = optimize_portfolio(annual_returns.values,covariance_matrix.values,)
    display_allocation(result)