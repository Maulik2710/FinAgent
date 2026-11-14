from app.data_pipeline.logger import logger
from app.data_pipeline.config import STOCKS

from app.forecasting.pipeline import forecast_pipeline
from app.news.pipeline import news_sentiment_pipeline
from app.portfolio.pipeline import portfolio_optimization_pipeline

from app.recommendation.engine import generate_recommendation


def recommendation_pipeline(symbol: str) -> dict:
    """
    Complete recommendation pipeline.

    If one module fails (no news key, model not trained, ...), its signal
    counts as neutral and the recommendation is still produced; the failed
    modules are listed in result["unavailable"].
    """
    symbol = symbol.upper()

    if symbol not in STOCKS:
        raise ValueError(f"Unknown symbol '{symbol}'. Available: {', '.join(STOCKS)}")

    logger.info(f"Generating recommendation for {symbol}...")

    unavailable = []

    current_price = predicted_price = predicted_return = None
    sentiment_score = None
    portfolio_weight = None

    # Forecast
    try:
        forecast = forecast_pipeline(symbol)
        current_price = float(forecast["current_price"])
        predicted_price = float(forecast["predicted_price"])
        predicted_return = (predicted_price - current_price) / current_price
    except Exception as e:
        logger.warning(f"{symbol}: forecast unavailable: {e}")
        unavailable.append("forecast")

    # News
    try:
        news = news_sentiment_pipeline(symbol)
        sentiment_score = float(news["score"])
    except Exception as e:
        logger.warning(f"{symbol}: news unavailable: {e}")
        unavailable.append("news")

    # Portfolio (look the weight up BY SYMBOL; never fall back to another stock)
    try:
        portfolio = portfolio_optimization_pipeline()
        weights = portfolio.get("weights_by_symbol") or dict(
            zip(portfolio["symbols"], portfolio["weights"])
        )
        if symbol in weights:
            portfolio_weight = float(weights[symbol])
        else:
            unavailable.append("portfolio")
    except Exception as e:
        logger.warning(f"{symbol}: portfolio unavailable: {e}")
        unavailable.append("portfolio")

    if len(unavailable) == 3:
        raise RuntimeError(
            "Could not generate a recommendation: forecast, news and portfolio "
            "are all unavailable. Check the logs."
        )

    result = generate_recommendation(
        predicted_return=predicted_return,
        sentiment_score=sentiment_score,
        portfolio_weight=portfolio_weight,
    )

    # Everything the API / frontend needs, so nothing has to be recomputed
    result.update({
        "symbol": symbol,
        "current_price": current_price,
        "predicted_price": predicted_price,
        "predicted_return": predicted_return,      # fraction, e.g. 0.008 = +0.8%
        "sentiment_score": sentiment_score,
        "portfolio_weight": portfolio_weight,      # fraction, e.g. 0.18 = 18%
        "unavailable": unavailable,
    })

    return result


# This is only for testing purposes
if __name__ == "__main__":

    recommendation = recommendation_pipeline("AAPL")

    print()
    print("Recommendation")
    print("-" * 40)
    print(f"Action       : {recommendation['recommendation']}")
    print(f"Confidence   : {recommendation['confidence']:.2f}%")
    print(f"Score        : {recommendation['score']:.2f}")

    print("\nReasons")
    for reason in recommendation["reasons"]:
        print(f"- {reason}")

    if recommendation["unavailable"]:
        print(f"\nUnavailable modules: {recommendation['unavailable']}")

    print(f"\n{recommendation['disclaimer']}")