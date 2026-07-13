from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint
)
from pathlib import Path

from app.data_pipeline.logger import logger
from app.data_pipeline.config import STOCKS

from app.forecasting.dataset import(
    load_processed_data,
    select_features,
    scale_features,
    create_sequences,
    split_train_test
)
from app.forecasting.model import build_lstm_model
from app.forecasting.config import(
    EPOCHS,
    BATCH_SIZE,
    VALIDATION_SPLIT,
    MODEL_NAME,
    SCALER_NAME,
)

import pickle
import numpy as np


MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR/MODEL_NAME
SCALER_PATH = MODEL_DIR/SCALER_NAME

def save_scaler(scaler) ->None:
    """ 
    Save the fitted scaller to disk.
    """
    
    MODEL_DIR.mkdir(exist_ok = True)
    
    with open(SCALER_PATH, "wb") as file:
        pickle.dump(scaler, file)
    

def train_model(symbol: str):
    """ 
    Train an LSTM model for a stock.
    """
    logger.info(f"Training model for {symbol}...")
    
    df = load_processed_data(symbol)
    
    df = select_features(df)
    
    print("=" * 50)
    print(df.isnull().sum())
    print("=" * 50)

    print("Any NaN:", df.isnull().values.any())
    print("Any Inf:", np.isinf(df.select_dtypes(include=[float, int])).values.any())
        
    scaled_data,scaler = scale_features(df)
        
    print("=" * 50)
    print("Scaled Data Debug")
    print("=" * 50)

    print("Shape:", scaled_data.shape)
    print("NaN Count:", np.isnan(scaled_data).sum())
    print("Inf Count:", np.isinf(scaled_data).sum())
    print("Min:", np.nanmin(scaled_data))
    print("Max:", np.nanmax(scaled_data))
        
    X,y = create_sequences(scaled_data)
    
    print("=" * 50)
    print("Sequence Debug")
    print("=" * 50)

    print("X NaN:", np.isnan(X).sum())
    print("y NaN:", np.isnan(y).sum())

    print("X Inf:", np.isinf(X).sum())
    print("y Inf:", np.isinf(y).sum())
    
    X_train, X_test, y_train, y_test = split_train_test(X,y)
    
    model = build_lstm_model(input_shape=(X_train.shape[1],X_train.shape[2]))
    
    early_stopping = EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    )
    
    checkpoint = ModelCheckpoint(
        filepath=MODEL_PATH,
        monitor="val_loss",
        save_best_only=True
    )
    
    history = model.fit(
        X_train,
        y_train,
        epochs = EPOCHS,
        batch_size = BATCH_SIZE,
        validation_split = VALIDATION_SPLIT,
        verbose = 1,
        callbacks = [
            early_stopping,
            checkpoint
        ]
    )
    
    logger.info(f"{symbol} model trained successfully.")
    
    save_scaler(scaler)
    logger.info("Scaler saved successfully.")
    
    
    
    return {
    "model": model,
    "history": history,
    "scaler": scaler,
    "X_test": X_test,
    "y_test": y_test,
}

# For Testing pupose Only
if __name__ == "__main__":

    for symbol in STOCKS:
        print(f"\nTraining {symbol}...")
        train_model(symbol)

