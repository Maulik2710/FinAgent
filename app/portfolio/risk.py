# Given a portfolio allocation, how risky is it and how good is it?

import numpy as np

from app.portfolio.config import RISK_FREE_RATE

def calculate_portfolio_return(weights: np.ndarray, annual_returns: np.ndarray) -> float:
    """
    Calculate expected portfolio return. 
    > Rp = Summation_from_i=1_to_n(wi*Ri) , 
    wi = weight of stock,
    Ri = expected annual return
    """

    return np.dot(weights, annual_returns)

def calculate_portfolio_volatility(weights: np.ndarray, covariance_matrix: np.ndarray) -> float:
    """
    Calculate portfolio volatility. 
    > {sigma}p = sqrt(wT * covariance Matrix * w)
    w = weights
    """

    return np.sqrt(weights.T @ covariance_matrix @ weights)

def calculate_sharpe_ratio(portfolio_return: float, portfolio_volatility: float) -> float:
    """
    Calculate Sharpe Ratio. --> (Rp - Rf)/{sigma}p
    """

    return (portfolio_return - RISK_FREE_RATE) / portfolio_volatility


#This is Only for the Testing Purpose
if __name__ == "__main__":

    from app.portfolio.metrics import (
        load_close_prices,
        calculate_daily_returns,
        calculate_annual_returns,
        calculate_covariance_matrix
    )

    from app.data_pipeline.config import STOCKS
    
    prices = load_close_prices(STOCKS)
    returns = calculate_daily_returns(prices)
    annual_returns = calculate_annual_returns(returns)
    covariance = calculate_covariance_matrix(returns)
    weights = np.ones(len(STOCKS)) / len(STOCKS)
    portfolio_return = calculate_portfolio_return(weights,annual_returns.values)
    portfolio_volatility = calculate_portfolio_volatility(weights,covariance.values)
    sharpe = calculate_sharpe_ratio(portfolio_return,portfolio_volatility)
    print(f"Return     : {portfolio_return:.4f}")
    print(f"Volatility : {portfolio_volatility:.4f}")
    print(f"Sharpe     : {sharpe:.4f}")