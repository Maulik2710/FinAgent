import pickle

import numpy as np

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


def load_saved_scaler():
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


def inverse_transform_predictions(scaler,predictions: np.ndarray):
    """
    Convert scaled predictions back to actual prices.
    """
    logger.info("Converting predictions back to original scale...")
    
    return scaler.inverse_transform(predictions)

def inverse_transform_targets(scaler,y_test: np.ndarray):
    """ 
    Convert scaled target values back to actual prices.
    """
    
    logger.info("Converting actual values back to original scale...")
    y_test = y_test.reshape(-1, 1)
    y_test = scaler.inverse_transform(y_test)

    return y_test

# # Testing Purpose 

# if __name__ == "__main__":

#     from app.forecasting.trainer import train_model
#     results = train_model("AAPL")
#     model = load_trained_model()
#     scaler = load_saved_scaler()
#     predictions = predict_prices(model,results["X_test"])
#     predictions = inverse_transform_predictions(scaler,predictions)
#     print(predictions[:5])