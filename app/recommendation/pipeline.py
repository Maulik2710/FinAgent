from app.data_pipeline.logger import logger

from app.recommendation.engine import generate_recommendation


def recommendation_pipeline(current_price: float, predicted_price: float, sentiment_score: float, portfolio_weight: float,):
    """
    Run the complete recommendation pipeline.
    """

    logger.info("Generating investment recommendation...")

    # Calculate predicted return
    predicted_return = (predicted_price - current_price) / current_price

    result = generate_recommendation(
        predicted_return=predicted_return,
        sentiment_score=sentiment_score,
        portfolio_weight=portfolio_weight,
    )

    logger.info("Recommendation generated successfully.")

    return result


# This is Only for the Testing Purpose
if __name__ == "__main__":

    current_price = 220.0
    predicted_price = 245.0
    sentiment_score = 0.60
    portfolio_weight = 0.18
    recommendation = recommendation_pipeline(
        current_price=current_price,
        predicted_price=predicted_price,
        sentiment_score=sentiment_score,
        portfolio_weight=portfolio_weight,
    )
    print()
    print("Recommendation")
    print("-" * 40)
    print(f"Action       : {recommendation['recommendation']}")
    print(f"Confidence   : {recommendation['confidence']}%")
    print(f"Score        : {recommendation['score']}")
    print("\nReasons")
    for reason in recommendation["reasons"]:
        print(f"- {reason}")