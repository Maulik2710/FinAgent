from app.recommendation.config import (
    BULLISH_THRESHOLD,
    BEARISH_THRESHOLD,
    POSITIVE_SENTIMENT,
    NEGATIVE_SENTIMENT,
    HIGH_ALLOCATION,
    LOW_ALLOCATION,
    FORECAST_WEIGHT,
    NEWS_WEIGHT,
    PORTFOLIO_WEIGHT,
)


def forecast_signal(predicted_return: float):
    """
    Generate a signal from the forecasted return.
    """

    if predicted_return >= BULLISH_THRESHOLD:
        return 1, "Forecast indicates a bullish trend."

    elif predicted_return <= BEARISH_THRESHOLD:
        return -1, "Forecast indicates a bearish trend."

    return 0, "Forecast is neutral."


def news_signal(sentiment_score: float):
    """
    Generate a signal from the news sentiment.
    """

    if sentiment_score >= POSITIVE_SENTIMENT:
        return 1, "News sentiment is positive."

    elif sentiment_score <= NEGATIVE_SENTIMENT:
        return -1, "News sentiment is negative."

    return 0, "News sentiment is neutral."


def portfolio_signal(weight: float):
    """
    Generate a signal from the recommended portfolio allocation.
    """

    if weight >= HIGH_ALLOCATION:
        return 1, "Portfolio optimizer recommends a high allocation."

    elif weight <= LOW_ALLOCATION:
        return -1, "Portfolio optimizer recommends a low allocation."

    return 0, "Portfolio allocation is moderate."


def generate_recommendation(
    predicted_return: float,
    sentiment_score: float,
    portfolio_weight: float,
):
    """
    Generate the final investment recommendation.
    """

    reasons = []

    # Forecast
    forecast_score, reason = forecast_signal(predicted_return)
    reasons.append(reason)

    # News 
    news_score, reason = news_signal(sentiment_score)
    reasons.append(reason)

    # Portfolio 
    portfolio_score, reason = portfolio_signal(portfolio_weight)
    reasons.append(reason)

    #  Weighted Score 
    total_score = (
        forecast_score * FORECAST_WEIGHT
        + news_score * NEWS_WEIGHT
        + portfolio_score * PORTFOLIO_WEIGHT
    )

    # Recommendation
    if total_score >= 0.8:
        recommendation = "Strong Buy"

    elif total_score >= 0.3:
        recommendation = "Buy"

    elif total_score > -0.3:
        recommendation = "Hold"

    elif total_score > -0.8:
        recommendation = "Sell"

    else:
        recommendation = "Strong Sell"

    # Confidence 
    confidence = round(abs(total_score) * 100, 2)

    return {
        "recommendation": recommendation,
        "confidence": confidence,
        "score": round(total_score, 2),
        "reasons": reasons,
    }


# This is Only for Testing purpose

# if __name__ == "__main__":

#     result = generate_recommendation(
#         predicted_return=0.08,
#         sentiment_score=0.60,
#         portfolio_weight=0.18,
#     )

#     print(result)