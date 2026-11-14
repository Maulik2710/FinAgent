import numpy as np

from app.data_pipeline.logger import logger

from app.forecasting.dataset import prepare_data
from app.forecasting.predictor import (
    load_trained_model,
    load_saved_scaler,
    predict_returns,
)


def forecast_pipeline(symbol: str):
    """
    Complete forecasting pipeline for one symbol.

    Returns
    -------
    dict with:
      current_price   : latest real close
      predicted_price : REAL next-day forecast (from the latest 60 days)
      actual_prices   : test-period real prices (backtest)
      predictions     : test-period predicted prices (backtest)
      prev_close      : previous-day close for each backtest point
    """
    logger.info(f"Running forecasting pipeline for {symbol}...")

    model = load_trained_model(symbol)
    scaler = load_saved_scaler(symbol)

    data = prepare_data(symbol, scaler=scaler)

    # Backtest: predicted price = previous real close * exp(predicted return)
    pred_returns = predict_returns(model, data["X_test"])
    predictions = data["prev_close_test"] * np.exp(pred_returns)
    actual_prices = data["actual_test"]

    # Real next-day forecast
    next_return = predict_returns(model, data["last_window"][None, ...])[0]
    current_price = data["last_close"]
    predicted_price = float(current_price * np.exp(next_return))

    logger.info(
        f"Forecast completed for {symbol}. "
        f"Current: ${current_price:.2f}, "
        f"Next-day predicted: ${predicted_price:.2f}"
    )

    return {
        "current_price": current_price,
        "predicted_price": predicted_price,
        "actual_prices": actual_prices,
        "predictions": predictions,
        "prev_close": data["prev_close_test"],
    }


# Testing only
if __name__ == "__main__":
    from app.forecasting.evaluator import evaluate_model

    symbol = "NVDA"
    result = forecast_pipeline(symbol)

    print("\nForecast Results")
    print("-----------------------------")
    print(f"Current Price        : ${result['current_price']:.2f}")
    print(f"Next-day Prediction  : ${result['predicted_price']:.2f}\n")

    evaluate_model(
        result["actual_prices"],
        result["predictions"],
        result["prev_close"],
    )
