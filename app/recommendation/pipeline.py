from app.data_pipeline.logger import logger

from app.forecasting.pipeline import forecast_pipeline
from app.news.pipeline import news_sentiment_pipeline
from app.portfolio.pipeline import portfolio_optimization_pipeline

from app.recommendation.engine import generate_recommendation


def recommendation_pipeline(symbol: str):
    """
    Complete recommendation pipeline.
    """

    logger.info(f"Generating recommendation for {symbol}...")

    # Forecast
    forecast = forecast_pipeline(symbol)

    current_price = forecast["current_price"]
    predicted_price = forecast["predicted_price"]

    # News
    news = news_sentiment_pipeline(symbol)
    sentiment_score = news["score"]

    # Portfolio
    portfolio = portfolio_optimization_pipeline()
    symbol_index = 0
    for symbol_idx,symbols in enumerate(portfolio["symbols"]):
        if symbols == symbol:
            symbol_index = symbol_idx
            break
    portfolio_weight = portfolio["weights"][symbol_index]

    predicted_return = (predicted_price - current_price) / current_price

    result = generate_recommendation(
        predicted_return=predicted_return,
        sentiment_score=sentiment_score,
        portfolio_weight=portfolio_weight,
    )

    return result


# This is Only for the Testing Purpose
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