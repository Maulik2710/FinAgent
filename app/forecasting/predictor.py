import pickle

import numpy as np

from sklearn.preprocessing import MinMaxScaler

from tensorflow.keras.models import load_model, Sequential

from app.data_pipeline.logger import logger

from app.forecasting.config import (
    MODEL_NAME,
    SCALER_NAME
)

from pathlib import Path

MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / MODEL_NAME
SCALER_PATH = MODEL_DIR / SCALER_NAME

def load_trained_model() -> Sequential:
    """
    Load the trained LSTM model.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            "Trained model not found. Train the model first."
        )

    logger.info("Loading trained model...")

    return load_model(MODEL_PATH)


def load_saved_scaler() -> MinMaxScaler:
    """
    Load the saved scaler.
    """
    if not SCALER_PATH.exists():
        raise FileNotFoundError(
            "Scaler not found. Train the model first."
        )
    
    logger.info("Loading scaler...")

    with open(SCALER_PATH, "rb") as file:
        scaler = pickle.load(file)

    return scaler


def predict_prices(model : Sequential,X_test: np.ndarray):
    """
    Predict scaled stock prices.
    """

    logger.info("Generating predictions...")
    predictions = model.predict(X_test)

    return predictions


def inverse_transform_predictions(scaler: MinMaxScaler, predictions: np.ndarray):
    """
    Convert scaled Close-price predictions back to the original price scale.
    """

    logger.info("Converting predictions back to original scale...")

    dummy = np.zeros((predictions.shape[0], scaler.n_features_in_))

    # Put predicted Close values in column 0
    dummy[:, 0] = predictions.flatten()

    # Inverse transform all features
    dummy = scaler.inverse_transform(dummy)

    # Return only the Close column
    return dummy[:, 0].reshape(-1, 1)

def inverse_transform_targets(scaler: MinMaxScaler,y_test: np.ndarray):
    """
    Convert scaled Close targets back to the original price scale.
    """

    logger.info("Converting actual values back to original scale...")

    y_test = y_test.reshape(-1, 1)

    dummy = np.zeros((y_test.shape[0], scaler.n_features_in_))

    dummy[:, 0] = y_test.flatten()

    dummy = scaler.inverse_transform(dummy)

    return dummy[:, 0].reshape(-1, 1)

# # Testing Purpose 
if __name__ == "__main__":
    from app.forecasting.dataset import (
        load_processed_data,
        select_features,
        scale_features,
        create_sequences,
        split_train_test,
    )

    symbol = "AAPL"

    # Load saved model and scaler
    model = load_trained_model()
    scaler = load_saved_scaler()

    # Load processed data
    df = load_processed_data(symbol)
    df = select_features(df)

    # Scale using the SAVED scaler
    scaled_data, _ = scale_features(df, scaler=scaler)

    # Create sequences
    X, y = create_sequences(scaled_data)

    # Get testing data
    _, X_test, _, y_test = split_train_test(X, y)

    # Predict
    predictions = predict_prices(model, X_test)

    # Convert back to actual prices
    predictions = inverse_transform_predictions(scaler, predictions)
    y_test = inverse_transform_targets(scaler, y_test)

    print(predictions[:5])