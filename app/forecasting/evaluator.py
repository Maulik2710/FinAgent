import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
    r2_score,
)

from app.data_pipeline.logger import logger


def calculate_mae(y_true, y_pred) -> float:
    return mean_absolute_error(y_true, y_pred)


def calculate_rmse(y_true, y_pred) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def calculate_mape(y_true, y_pred) -> float:
    return mean_absolute_percentage_error(y_true, y_pred) * 100


def calculate_r2(y_true, y_pred) -> float:
    return r2_score(y_true, y_pred)


def calculate_directional_accuracy(y_true, y_pred, prev_close) -> float:
    """% of days where the predicted direction (up/down) was correct."""
    true_dir = np.sign(y_true - prev_close)
    pred_dir = np.sign(y_pred - prev_close)
    return float(np.mean(true_dir == pred_dir)) * 100


def naive_baseline_mae(y_true, prev_close) -> float:
    """MAE of the 'tomorrow = today' baseline. The model must beat this."""
    return mean_absolute_error(y_true, prev_close)


def plot_predictions(y_true, y_pred, last_n: int = 100):
    plt.figure(figsize=(12, 6))
    plt.plot(y_true[-last_n:], label="Actual")
    plt.plot(y_pred[-last_n:], label="Predicted", linestyle="--")
    plt.xlabel("Days")
    plt.ylabel("Close Price")
    plt.title("Actual vs Predicted Stock Price")
    plt.legend()
    plt.show()


def evaluate_model(y_true, y_pred, prev_close, plot: bool = True):
    """Compute all metrics, compare with the naive baseline, optionally plot."""
    logger.info("Evaluating model...")

    y_true = np.asarray(y_true).flatten()
    y_pred = np.asarray(y_pred).flatten()
    prev_close = np.asarray(prev_close).flatten()

    mae = calculate_mae(y_true, y_pred)
    rmse = calculate_rmse(y_true, y_pred)
    mape = calculate_mape(y_true, y_pred)
    r2 = calculate_r2(y_true, y_pred)
    dir_acc = calculate_directional_accuracy(y_true, y_pred, prev_close)
    base_mae = naive_baseline_mae(y_true, prev_close)

    print(f"MAE              : {mae:.4f}")
    print(f"Naive baseline MAE: {base_mae:.4f}  "
          f"({'model BEATS baseline' if mae < base_mae else 'model does NOT beat baseline'})")
    print(f"RMSE             : {rmse:.4f}")
    print(f"MAPE             : {mape:.2f}%")
    print(f"R2 score         : {r2:.4f}")
    print(f"Directional acc. : {dir_acc:.2f}%")

    if plot:
        plot_predictions(y_true, y_pred)

    return {
        "MAE": mae,
        "Naive_MAE": base_mae,
        "RMSE": rmse,
        "MAPE": mape,
        "R2_score": r2,
        "Directional_Accuracy": dir_acc,
    }
