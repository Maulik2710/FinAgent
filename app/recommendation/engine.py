import math

from app.recommendation.config import (
    BULLISH_THRESHOLD,
    BEARISH_THRESHOLD,
    FORECAST_HORIZON_LABEL,
    POSITIVE_SENTIMENT,
    NEGATIVE_SENTIMENT,
    HIGH_ALLOCATION,
    LOW_ALLOCATION,
    FORECAST_WEIGHT,
    NEWS_WEIGHT,
    PORTFOLIO_WEIGHT,
    BUY_SCORE,
    STRONG_BUY_SCORE,
    DISCLAIMER,
)


def _is_valid(value) -> bool:
    """True for a real, finite number (False for None / NaN / inf)."""
    try:
        return value is not None and math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def forecast_signal(predicted_return: float):
    """
    Generate a signal from the forecasted return.
    """
    if not _is_valid(predicted_return):
        return 0, "Forecast is unavailable."

    move = f"{predicted_return:+.2%} expected {FORECAST_HORIZON_LABEL} move"

    if predicted_return >= BULLISH_THRESHOLD:
        return 1, f"Forecast indicates a bullish trend ({move})."

    elif predicted_return <= BEARISH_THRESHOLD:
        return -1, f"Forecast indicates a bearish trend ({move})."

    return 0, f"Forecast is neutral ({move})."


def news_signal(sentiment_score: float):
    """
    Generate a signal from the news sentiment.
    """
    if not _is_valid(sentiment_score):
        return 0, "News sentiment is unavailable."

    if sentiment_score >= POSITIVE_SENTIMENT:
        return 1, f"News sentiment is positive (score {sentiment_score:+.2f})."

    elif sentiment_score <= NEGATIVE_SENTIMENT:
        return -1, f"News sentiment is negative (score {sentiment_score:+.2f})."

    return 0, f"News sentiment is neutral (score {sentiment_score:+.2f})."


def portfolio_signal(weight: float):
    """
    Generate a signal from the recommended portfolio allocation.
    """
    if not _is_valid(weight):
        return 0, "Portfolio allocation is unavailable for this stock."

    if weight >= HIGH_ALLOCATION:
        return 1, f"Portfolio optimizer recommends a high allocation ({weight:.1%})."

    elif weight <= LOW_ALLOCATION:
        return -1, f"Portfolio optimizer recommends a low allocation ({weight:.1%})."

    return 0, f"Portfolio allocation is moderate ({weight:.1%})."


def _label(total_score: float) -> str:
    if total_score >= STRONG_BUY_SCORE:
        return "Strong Buy"
    elif total_score >= BUY_SCORE:
        return "Buy"
    elif total_score > -BUY_SCORE:
        return "Hold"
    elif total_score > -STRONG_BUY_SCORE:
        return "Sell"
    return "Strong Sell"


def generate_recommendation(
    predicted_return: float,
    sentiment_score: float,
    portfolio_weight: float,
):
    """
    Generate the final investment recommendation.

    Any input may be None / NaN when that module is unavailable: its signal
    then counts as neutral and the reasons say so.
    """
    forecast_score, forecast_reason = forecast_signal(predicted_return)
    news_score, news_reason = news_signal(sentiment_score)
    portfolio_score, portfolio_reason = portfolio_signal(portfolio_weight)

    reasons = [forecast_reason, news_reason, portfolio_reason]

    # Weighted score in [-1, 1] (divided by the weight sum, so changing the
    # weights in config can never push the score outside that range)
    total_weight = FORECAST_WEIGHT + NEWS_WEIGHT + PORTFOLIO_WEIGHT

    total_score = (
        forecast_score * FORECAST_WEIGHT
        + news_score * NEWS_WEIGHT
        + portfolio_score * PORTFOLIO_WEIGHT
    ) / total_weight

    total_score = round(total_score, 6)   # avoids float edge cases like 0.39999999

    recommendation = _label(total_score)

    # Confidence (a heuristic, not a probability):
    #  - Buy / Sell : how strong the combined signal is
    #  - Hold       : how far the score is from the Buy / Sell boundary
    #                 (all signals neutral = high, conflicting signals = low)
    if recommendation == "Hold":
        confidence = (1 - abs(total_score) / BUY_SCORE) * 100
    else:
        confidence = abs(total_score) * 100

    confidence = round(min(max(confidence, 0.0), 100.0), 2)

    return {
        "recommendation": recommendation,
        "confidence": confidence,
        "score": round(total_score, 2),
        "reasons": reasons,
        "signals": {
            "forecast": forecast_score,
            "news": news_score,
            "portfolio": portfolio_score,
        },
        "disclaimer": DISCLAIMER,
    }


# This is only for testing purposes
if __name__ == "__main__":

    result = generate_recommendation(
        predicted_return=0.008,
        sentiment_score=0.60,
        portfolio_weight=0.18,
    )

    print(result)