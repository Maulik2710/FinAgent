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
    Load raw stock data for a given symbol (sorted oldest -> newest).
    """
    file_path = RAW_DATA_DIR / f"{symbol}.csv"

    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw data for {symbol} not found. Run the downloader first."
        )

    logger.info(f"Loading {symbol} data...")

    df = pd.read_csv(file_path)

    if "Date" not in df.columns:
        raise ValueError(f"{symbol}: 'Date' column not found in raw data.")

    df["Date"] = pd.to_datetime(df["Date"])
    df = (
        df.drop_duplicates(subset="Date", keep="last")
        .sort_values("Date")
        .reset_index(drop=True)
    )

    return df


def save_processed_data(df: pd.DataFrame, symbol: str) -> None:
    """
    Save the processed data (Date stored as YYYY-MM-DD text).
    """
    file_path = PROCESSED_DATA_DIR / f"{symbol}.csv"

    df = df.copy()
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

    df.to_csv(file_path, index=False)
    logger.info(f"{symbol} saved to processed data ({len(df)} rows).")


def engineer_features_pipeline() -> dict:
    """
    Generate technical indicators for all the stocks.
    Returns {"success": [...], "failed": [...]}.
    """
    success, failed = [], []

    for symbol in STOCKS:

        logger.info(f"Engineering features for {symbol}...")

        try:
            df = load_stock_data(symbol)
            raw_rows = len(df)

            df = engineer_features(df)

            save_processed_data(df, symbol)

            logger.info(
                f"{symbol} completed: {raw_rows} raw rows -> {len(df)} processed rows."
            )
            success.append(symbol)

        except Exception as e:
            logger.exception(f"Failed to engineer features for {symbol}: {e}")
            failed.append(symbol)

    logger.info(f"Feature engineering done. Success: {success}")
    if failed:
        logger.warning(f"Failed: {failed}")

    return {"success": success, "failed": failed}


if __name__ == "__main__":

    logger.info("Starting feature engineering pipeline...")

    engineer_features_pipeline()

    logger.info("Feature engineering completed successfully.")