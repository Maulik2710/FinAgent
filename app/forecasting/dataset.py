import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler

from app.data_pipeline.config import PROCESSED_DATA_DIR
from app.data_pipeline.logger import logger

from app.forecasting.config import SEQUENCE_LENGTH , TRAIN_SPLIT , FEATURE_COLUMNS


def load_processed_data(symbol:str) -> pd.DataFrame:
    """ 
    Load Processed stock Data.
    """
    
    file_path = PROCESSED_DATA_DIR / f"{symbol}.csv"
    
    logger.info(f"Loading processed data for {symbol}")
    
    return pd.read_csv(file_path)

def select_features(df: pd.DataFrame) ->pd.DataFrame:
    """ 
    Select Feature used for forecasting.
    """
    
    return df[FEATURE_COLUMNS]

def scale_features(df, scaler=None):
    """
    Scale features using MinMaxScaler.

    Parameters
    ----------
    df : pd.DataFrame
        Feature dataframe.

    scaler : MinMaxScaler | None
        If None, fit a new scaler.
        Otherwise use the provided fitted scaler.

    Returns
    -------
    scaled_data
    scaler
    """

    if scaler is None:
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(df)
    else:
        scaled_data = scaler.transform(df)

    return scaled_data, scaler


def create_sequences(scaled_data: np.ndarray,sequence_length: int = SEQUENCE_LENGTH):
    """ 
    Create input-output sequences for the LSTM model.
    """
    
    X = []
    y = []
    
    for i in range(sequence_length,len(scaled_data)):
        
        X.append(scaled_data[i-sequence_length:i])
        
        y.append(scaled_data[i,0])
        
    X = np.array(X)
    y = np.array(y)
    
    return X,y

def split_train_test(X: np.ndarray, y: np.ndarray,train_split: float = TRAIN_SPLIT):
    """ 
    Split the dataset into training and testing sets while preserving the chronological order.
    """
    
    split_index = int(len(X) * train_split)
    
    X_train = X[:split_index]
    X_test = X[split_index:]
    
    y_train = y[:split_index]
    y_test = y[split_index:]
    
    return X_train,X_test,y_train,y_test


# Just for Training Purpose

df = load_processed_data("AAPL")
df = select_features(df)
scaled_data, scaler = scale_features(df)
X, y = create_sequences(scaled_data)
print(X.shape)
print(y.shape)
X_train, X_test, y_train, y_test = split_train_test(X, y)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)