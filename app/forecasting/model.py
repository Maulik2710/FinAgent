from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import Huber

from app.forecasting.config import (
    LSTM_UNITS,
    DROPOUT_RATE,
    LEARNING_RATE,
)


def build_lstm_model(input_shape: tuple) -> Sequential:
    """
    Build and compile a 2-layer LSTM that predicts the next log-return (%).

    Parameters
    ----------
    input_shape : (time_steps, n_features)
    """
    model = Sequential([
        Input(shape=input_shape),
        LSTM(LSTM_UNITS, return_sequences=True),
        Dropout(DROPOUT_RATE),
        LSTM(LSTM_UNITS // 2),
        Dropout(DROPOUT_RATE),
        Dense(25, activation="relu"),
        Dense(1),
    ])

    model.compile(
        optimizer=Adam(learning_rate=LEARNING_RATE),
        loss=Huber(),          # robust to fat-tailed returns
        metrics=["mae"],
    )

    return model
