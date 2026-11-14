import pickle
import random

import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

from app.data_pipeline.logger import logger
from app.data_pipeline.config import STOCKS

from app.forecasting.dataset import prepare_data
from app.forecasting.model import build_lstm_model
from app.forecasting.config import (
    EPOCHS,
    BATCH_SIZE,
    VALIDATION_SPLIT,
    EARLY_STOP_PATIENCE,
    RANDOM_SEED,
    get_paths,
)


def set_seed(seed: int = RANDOM_SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)


def train_model(symbol: str):
    """Train an LSTM for ONE stock and save its own model + scaler."""
    logger.info(f"Training model for {symbol}...")
    set_seed()

    model_path, scaler_path = get_paths(symbol)

    data = prepare_data(symbol)
    X_train, y_train = data["X_train"], data["y_train"]

    if np.isnan(X_train).any() or np.isnan(y_train).any():
        raise ValueError(f"NaN values found in training data for {symbol}")

    model = build_lstm_model(input_shape=(X_train.shape[1], X_train.shape[2]))

    callbacks = [
        EarlyStopping(
            monitor="val_loss",
            patience=EARLY_STOP_PATIENCE,
            restore_best_weights=True,
        ),
        ModelCheckpoint(
            filepath=str(model_path),
            monitor="val_loss",
            save_best_only=True,
        ),
    ]

    history = model.fit(
        X_train,
        y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_split=VALIDATION_SPLIT,
        shuffle=False,          # keep time order
        verbose=1,
        callbacks=callbacks,
    )

    with open(scaler_path, "wb") as file:
        pickle.dump(data["scaler"], file)

    logger.info(f"{symbol} model and scaler saved to {model_path.parent}")

    return {"model": model, "history": history, **data}


# For training from the command line
if __name__ == "__main__":
    for symbol in STOCKS:
        print(f"\nTraining {symbol}...")
        train_model(symbol)
