import numpy as np
from scipy.optimize import minimize

from app.data_pipeline.config import STOCKS
from app.data_pipeline.logger import logger

from app.portfolio.config import MAX_WEIGHT, MIN_WEIGHT

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
    calculate_portfolio_summary,
)


def negative_sharpe_ratio(
    weights: np.ndarray,
    annual_returns: np.ndarray,
    covariance_matrix: np.ndarray,
) -> float:
    """
    Objective function for optimization.
    Returns the negative Sharpe Ratio because scipy minimizes.
    """
    portfolio_return = calculate_portfolio_return(weights, annual_returns)
    portfolio_volatility = calculate_portfolio_volatility(weights, covariance_matrix)
    sharpe_ratio = calculate_sharpe_ratio(portfolio_return, portfolio_volatility)

    return -sharpe_ratio


def optimize_portfolio(
    annual_returns: np.ndarray,
    covariance_matrix: np.ndarray,
    symbols: list = None,
) -> dict:
    """
    Find the portfolio allocation that maximizes the Sharpe Ratio.

    - Long-only, weights sum to 1, no stock above MAX_WEIGHT.
    - `symbols` must match the order of annual_returns (defaults to STOCKS).
    - If the optimizer fails, equal weights are returned and "success" is False.
    """
    annual_returns = np.asarray(annual_returns, dtype=float)
    covariance_matrix = np.asarray(covariance_matrix, dtype=float)

    number_of_stocks = len(annual_returns)

    symbols = list(symbols) if symbols is not None else list(STOCKS)

    if len(symbols) != number_of_stocks:
        raise ValueError(
            f"{len(symbols)} symbols but {number_of_stocks} return values."
        )

    # The cap can never be below equal weight, otherwise no solution exists
    max_weight = max(MAX_WEIGHT, 1.0 / number_of_stocks)

    equal_weights = np.ones(number_of_stocks) / number_of_stocks

    constraints = (
        {"type": "eq", "fun": lambda weights: np.sum(weights) - 1},
    )

    bounds = tuple((0.0, max_weight) for _ in range(number_of_stocks))

    result = minimize(
        fun=negative_sharpe_ratio,
        x0=equal_weights,
        args=(annual_returns, covariance_matrix),
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
    )

    if result.success:
        weights = np.clip(result.x, 0.0, max_weight)
        weights[weights < MIN_WEIGHT] = 0.0
        weights = weights / weights.sum()
    else:
        logger.warning(
            f"Portfolio optimizer did not converge ({result.message}). "
            "Using equal weights."
        )
        weights = equal_weights

    summary = calculate_portfolio_summary(weights, annual_returns, covariance_matrix)

    return {
        "symbols": symbols,
        "weights": weights,
        "return": summary["return"],
        "volatility": summary["volatility"],
        "sharpe": summary["sharpe"],
        "success": bool(result.success),
    }


def display_allocation(result: dict) -> None:
    """
    Display the optimized portfolio allocation and statistics.
    """
    print("\nRecommended Portfolio Allocation\n")

    allocations = sorted(
        zip(result["symbols"], result["weights"]),
        key=lambda x: x[1],
        reverse=True,
    )

    for stock, weight in allocations:
        print(f"{stock:<6}: {weight * 100:.2f}%")

    print("\nPortfolio Statistics")
    print("-" * 30)
    print(f"Expected Return : {result['return']:.2%}")
    print(f"Volatility      : {result['volatility']:.2%}")
    print(f"Sharpe Ratio    : {result['sharpe']:.4f}")


# Only for testing purposes
if __name__ == "__main__":

    prices = load_close_prices(STOCKS)
    daily_returns = calculate_daily_returns(prices)
    annual_returns = calculate_annual_returns(daily_returns)
    covariance_matrix = calculate_covariance_matrix(daily_returns)

    result = optimize_portfolio(
        annual_returns.values,
        covariance_matrix.values,
        symbols=list(prices.columns),
    )

    print("Symbols:", result["symbols"])
    print("Weights:", np.round(result["weights"], 4))
    print("Weights sum:", result["weights"].sum())

    display_allocation(result)