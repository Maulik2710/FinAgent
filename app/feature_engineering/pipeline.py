import pandas as pd

from app.data_pipeline.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    STOCKS
)

from app.data_pipeline.logger import logger

from app.feature_engineering.indicators import engineer_features

def load_stock_data(symbol: str) -> pd.DataFrame:
    """ 
    Load raw stock data for a given symbol.
    """
    
    file_path = RAW_DATA_DIR / f"{symbol}.csv"
    logger.info(f"loading {symbol} data...")
    
    return pd.read_csv(file_path)

def save_processed_data(df: pd.DataFrame,symbol:str) -> None:
    """ 
    Save the processed data.
    """
    
    file_path = PROCESSED_DATA_DIR / f"{symbol}.csv"
    df.to_csv(file_path,index = False)
    logger.info(f"{symbol} save to processed data.")
    

def engineer_features_pipeline() -> None:
    """ 
    Generate Technicle indicator for all the stocks.
    """
    
    for symbol in STOCKS:
        
        logger.info(f"Engineering features for {symbol}...")
        try:
            df = load_stock_data(symbol)
            df = engineer_features(df)
            save_processed_data(df,symbol)
            logger.info(f"{symbol} completed successfully.")
        except Exception as e:
            logger.exception(f"Failed to engineer features for {symbol}: {e}")
        
    