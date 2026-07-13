import pandas as pd

def add_daily_return(df : pd.DataFrame) -> pd.DataFrame:
    """
    Add Daily Percentage Return.
    """
    
    if "Close" not in df.columns:
        raise ValueError("Close column not found.")
    df = df.copy()
    df["Daily_Return"] = df["Close"].pct_change()
    return df

def add_sma(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Adding Simple Moving Average.
    """
    
    if "Close" not in df.columns:
        raise ValueError("Close column not found.")
    df = df.copy()
    
    df[f"SMA_{window}"] = (
        df["Close"].rolling(window).mean()
    )
    
    return df

def add_ema(df: pd.DataFrame,window: int= 20) ->pd.DataFrame:
    """ 
    Adding Exponential Moving Average
    """
    
    if "Close" not in df.columns:
        raise ValueError("Close column not found.")
    
    df = df.copy()
    
    df[f"EMA_{window}"] = (
        df["Close"].ewm(span = window,adjust = False).mean() # ewm = Exponentially Weighted Moving
    )
    
    return df

def add_rsi(df: pd.DataFrame,
            window: int = 14) -> pd.DataFrame:
    """
    Add Relative Strength Index. 
    This column indicates whether the stock has been bought too aggressively (overbought) or sold too aggressively (oversold).
    RSI > 70 → Potentially overbought (price has risen strongly).
    RSI < 30 → Potentially oversold (price has fallen strongly).
    """

    if "Close" not in df.columns:
        raise ValueError("Close column not found.")

    df = df.copy()
    delta = df["Close"].diff() # How one day is different from another by closing prise.
    gain = delta.clip(lower=0) # Makes -ve value 0.
    loss = -delta.clip(upper=0) # How much loss we get from last Day.
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss
    df[f"RSI_{window}"] = 100 - (100 / (1 + rs))

    return df

def add_macd(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add Moving Average Convergence Divergence and Signal Line. MACD measures trend and momentum.
    This column indicates whether the trend is getting stronger or weaker.
    """

    if "Close" not in df.columns:
        raise ValueError("Close column not found.")

    df = df.copy()
    ema12 = df["Close"].ewm(span=12,
                            adjust=False).mean() 
    ema26 = df["Close"].ewm(span=26,
                            adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_Signal"] = (
        df["MACD"]
        .ewm(span=9,
             adjust=False)
        .mean()
    )

    return df

def add_rolling_volatility(df: pd.DataFrame,
                           window: int = 20) -> pd.DataFrame:
    """
    Add rolling volatility.
    """

    if "Daily_Return" not in df.columns:
        df = add_daily_return(df)
    df = df.copy()
    df["Rolling_Volatility"] = (
        df["Daily_Return"]
        .rolling(window)
        .std()
    )

    return df

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add all technical indicators.
    """

    df = add_daily_return(df)
    df = add_sma(df)
    df = add_ema(df)
    df = add_rsi(df)
    df = add_macd(df)
    df = add_rolling_volatility(df)

    df = df.dropna().reset_index(drop=True)
    return df