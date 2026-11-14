# Given a portfolio allocation, how risky is it and how good is it?

import numpy as np

from app.portfolio.config import RISK_FREE_RATE


def calculate_portfolio_return(weights: np.ndarray, annual_returns: np.ndarray) -> float:
    """
    Calculate expected portfolio return.
    > Rp = Summation_from_i=1_to_n(wi * Ri)
    wi = weight of stock, Ri = expected annual return
    """
    return float(np.dot(weights, annual_returns))


def calculate_portfolio_volatility(weights: np.ndarray, covariance_matrix: np.ndarray) -> float:
    """
    Calculate portfolio volatility.
    > sigma_p = sqrt(wT * covariance_matrix * w)
    """
    variance = weights.T @ covariance_matrix @ weights

    return float(np.sqrt(max(variance, 0.0)))


def calculate_sharpe_ratio(portfolio_return: float, portfolio_volatility: float) -> float:
    """
    Calculate Sharpe Ratio. --> (Rp - Rf) / sigma_p
    Returns 0.0 if the volatility is zero.
    """
    if portfolio_volatility <= 0:
        return 0.0

    return float((portfolio_return - RISK_FREE_RATE) / portfolio_volatility)


def calculate_portfolio_summary(
    weights: np.ndarray,
    annual_returns: np.ndarray,
    covariance_matrix: np.ndarray,
) -> dict:
    """
    Return, volatility and Sharpe ratio of a portfolio in one call.
    """
    weights = np.asarray(weights, dtype=float)

    portfolio_return = calculate_portfolio_return(weights, annual_returns)
    portfolio_volatility = calculate_portfolio_volatility(weights, covariance_matrix)
    sharpe = calculate_sharpe_ratio(portfolio_return, portfolio_volatility)

    return {
        "return": portfolio_return,
        "volatility": portfolio_volatility,
        "sharpe": sharpe,
    }


# Only for testing purposes
if __name__ == "__main__":

    from app.portfolio.metrics import (
        load_close_prices,
        calculate_daily_returns,
        calculate_annual_returns,
        calculate_covariance_matrix,
    )

    from app.data_pipeline.config import STOCKS

    prices = load_close_prices(STOCKS)
    returns = calculate_daily_returns(prices)
    annual_returns = calculate_annual_returns(returns)
    covariance = calculate_covariance_matrix(returns)
    weights = np.ones(len(STOCKS)) / len(STOCKS)

    summary = calculate_portfolio_summary(weights, annual_returns.values, covariance.values)
    print(f"Return     : {summary['return']:.4f}")
    print(f"Volatility : {summary['volatility']:.4f}")
    print(f"Sharpe     : {summary['sharpe']:.4f}")