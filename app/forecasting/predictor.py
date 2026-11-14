import pickle

import numpy as np
from tensorflow.keras.models import load_model

from app.data_pipeline.logger import logger
from app.forecasting.config import get_paths


def load_trained_model(symbol: str):
    """Load the trained LSTM for a specific symbol."""
    model_path, _ = get_paths(symbol)

    if not model_path.exists():
        raise FileNotFoundError(
            f"No trained model for {symbol}. Train it first."
        )

    logger.info(f"Loading trained model for {symbol}...")
    return load_model(model_path)


def load_saved_scaler(symbol: str):
    """Load the fitted scaler for a specific symbol."""
    _, scaler_path = get_paths(symbol)

    if not scaler_path.exists():
        raise FileNotFoundError(
            f"No scaler for {symbol}. Train it first."
        )

    logger.info(f"Loading scaler for {symbol}...")
    with open(scaler_path, "rb") as file:
        return pickle.load(file)


def predict_returns(model, X: np.ndarray) -> np.ndarray:
    """
    Predict log-returns as fractions (the model outputs percent).
    Price = previous_close * exp(return).
    """
    logger.info("Generating predictions...")
    preds = model.predict(X, verbose=0).flatten()
    return preds / 100.0


# Testing only
if __name__ == "__main__":
    from app.forecasting.dataset import prepare_data

    symbol = "AAPL"
    model = load_trained_model(symbol)
    scaler = load_saved_scaler(symbol)
    data = prepare_data(symbol, scaler=scaler)

    rets = predict_returns(model, data["X_test"])
    prices = data["prev_close_test"] * np.exp(rets)
    print(prices[:5])
