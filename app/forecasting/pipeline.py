from app.data_pipeline.logger import logger

from app.forecasting.dataset import (
    load_processed_data,
    select_features,
    scale_features,
    create_sequences,
    split_train_test,
)

from app.forecasting.predictor import (
    load_trained_model,
    load_saved_scaler,
    predict_prices,
    inverse_transform_predictions,
    inverse_transform_targets,
)


def forecast_pipeline(symbol: str):
    """
    Complete forecasting pipeline.
    """

    logger.info(f"Running forecasting pipeline for {symbol}...")

    # Load model & scaler
    model = load_trained_model()
    scaler = load_saved_scaler()

    # Load processed data
    df = load_processed_data(symbol)

    df = select_features(df)

    # Scale using SAVED scaler
    scaled_data, _ = scale_features(df, scaler=scaler,)

    # Create sequences
    X, y = create_sequences(scaled_data)
    
    _, X_test, _, y_test = split_train_test(X, y)

    # Predict
    predictions = predict_prices(model, X_test)

    # Back to original prices
    predictions = inverse_transform_predictions(scaler, predictions,)

    actual_prices = inverse_transform_targets(scaler, y_test)

    current_price = float(actual_prices[-1][0])

    predicted_price = float(predictions[-1][0])

    logger.info(
    f"Forecast completed for {symbol}. "
    f"Current: ${current_price:.2f}, "
    f"Predicted: ${predicted_price:.2f}"
)

    return {
        "current_price": current_price,
        "predicted_price": predicted_price,
        "actual_prices": actual_prices.flatten(),
        "predictions": predictions.flatten(),
    }


#This is Only for the testing purpose

if __name__ == "__main__":

    result = forecast_pipeline("AAPL")
    print()
    print("Forecast Results")
    print("-----------------------------")
    print(f"Current Price   : ${result['current_price']:.2f}")
    print(f"Predicted Price : ${result['predicted_price']:.2f}")