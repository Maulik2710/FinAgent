import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler

from app.data_pipeline.config import PROCESSED_DATA_DIR
from app.data_pipeline.logger import logger

from app.forecasting.config import (
    SEQUENCE_LENGTH,
    TRAIN_SPLIT,
    FEATURE_COLUMNS,
    REQUIRED_RAW_COLUMNS,
)


def load_processed_data(symbol: str) -> pd.DataFrame:
    """Load processed stock data."""
    file_path = PROCESSED_DATA_DIR / f"{symbol}.csv"
    logger.info(f"Loading processed data for {symbol}")
    return pd.read_csv(file_path)


def add_stationary_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build stationary features and the prediction target.

    Target = today's log return in percent. The model predicts the return,
    and the price is rebuilt as: previous_close * exp(return).
    """
    missing = [c for c in REQUIRED_RAW_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Processed data is missing columns: {missing}")

    df = df.copy()

    df["Close_SMA_Ratio"] = df["Close"] / df["SMA_20"] - 1
    df["Close_EMA_Ratio"] = df["Close"] / df["EMA_20"] - 1
    df["MACD_Norm"] = df["MACD"] / df["Close"]
    df["MACD_Signal_Norm"] = df["MACD_Signal"] / df["Close"]

    volume = df["Volume"].replace(0, np.nan)
    df["Volume_Change"] = np.log(volume).diff()

    df["Target"] = np.log(df["Close"] / df["Close"].shift(1)) * 100

    needed = FEATURE_COLUMNS + ["Target", "Close"]
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=needed).reset_index(drop=True)

    return df


def prepare_data(symbol: str, scaler=None):
    """
    Full data preparation for one symbol.

    - scaler is fit on TRAIN rows only (no leakage from the test period)
    - if a fitted scaler is passed (inference), it is only used to transform
    """
    df = add_stationary_features(load_processed_data(symbol))

    if len(df) < SEQUENCE_LENGTH + 50:
        raise ValueError(f"Not enough data for {symbol}: {len(df)} rows")

    features = df[FEATURE_COLUMNS].values
    target = df["Target"].values
    close = df["Close"].values

    n_seq = len(df) - SEQUENCE_LENGTH
    split = int(n_seq * TRAIN_SPLIT)
    train_rows = split + SEQUENCE_LENGTH  # rows seen by training sequences

    if scaler is None:
        scaler = StandardScaler().fit(features[:train_rows])
    scaled = scaler.transform(features)

    X, y, prev_close, actual = [], [], [], []
    for i in range(SEQUENCE_LENGTH, len(df)):
        X.append(scaled[i - SEQUENCE_LENGTH:i])
        y.append(target[i])
        prev_close.append(close[i - 1])
        actual.append(close[i])

    X = np.array(X)
    y = np.array(y)
    prev_close = np.array(prev_close)
    actual = np.array(actual)

    return {
        "X_train": X[:split],
        "y_train": y[:split],
        "X_test": X[split:],
        "y_test": y[split:],
        "prev_close_test": prev_close[split:],
        "actual_test": actual[split:],
        "last_window": scaled[-SEQUENCE_LENGTH:],  # for the real next-day forecast
        "last_close": float(close[-1]),
        "scaler": scaler,
    }


# Just for testing
if __name__ == "__main__":
    data = prepare_data("AAPL")
    for k in ["X_train", "y_train", "X_test", "y_test", "actual_test"]:
        print(k, data[k].shape)
