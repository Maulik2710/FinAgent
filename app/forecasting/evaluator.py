import numpy as np

import matplotlib.pyplot as plt

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
    r2_score
)

from app.data_pipeline.logger import logger

def calculate_mae(y_true: np.ndarray,y_pred: np.ndarray) -> float:
    """
    Calculate Mean Absolute Error.
    """

    return mean_absolute_error(y_true,y_pred)

def calculate_rmse(y_true: np.ndarray,y_pred: np.ndarray) -> float:
    """
    Calculate Root Mean Squared Error.
    """

    mse = mean_squared_error(y_true,y_pred)

    return np.sqrt(mse)

def calculate_mape(y_true: np.ndarray,y_pred: np.ndarray) -> float:
    """
    Calculate Mean Absolute Percentage Error.
    """

    return mean_absolute_percentage_error(y_true,y_pred) * 100

def calculate_r2(y_true, y_pred):
    """ 
    Calculate r2_score
    """
    return r2_score(y_true, y_pred)

def plot_predictions(y_true,y_pred):
    """ 
    Plot the graph for actual value and predicted values.
    """
    plt.figure(figsize=(12,6))
    plt.plot(y_true,label="Actual")
    plt.plot(y_pred,label="Predicted")
    plt.xlabel("Days")
    plt.ylabel("Close Price")
    plt.title("Actual vs Predicted Stock Price")
    plt.legend()
    plt.show()
    
def evaluate_model(y_true,y_pred):
    """ 
    This Function Combines Everything in One.
    """
    
    logger.info("Evaluating model...")
    
    mae = calculate_mae(y_true,y_pred)
    print(f"MAE  : {mae:.4f}")

    rmse = calculate_rmse(y_true,y_pred)
    print(f"RMSE : {rmse:.4f}")

    mape = calculate_mape(y_true,y_pred)
    print(f"MAPE : {mape:.2f}%")
    
    r2_Score = calculate_r2(y_true,y_pred)
    print(f"R2_score : {r2_Score:.2f}%")
    
    plot_predictions(y_true,y_pred)
    
    return {
        "MAE": mae,
        "RMSE": rmse,
        "MAPE": mape,
        "R2_score" : r2_Score
    }
        



    