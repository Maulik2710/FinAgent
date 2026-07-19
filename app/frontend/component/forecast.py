import streamlit as st
import matplotlib.pyplot as plt
from app.forecasting.pipeline import forecast_pipeline

def plot(symbol: str,actual_prices: list,predictions: list):
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        actual_prices,
        label="Actual Price",
        linewidth=2,
    )

    ax.plot(
        predictions,
        "--",
        label="Predicted Price",
        linewidth=2,
    )

    ax.set_title(f"{symbol} Stock Price Forecast")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price ($)")

    ax.legend()

    st.pyplot(fig)
    
def show_forecast(symbol: str):
    """
    Display the forecast page.
    """

    st.header("📈 Stock Price Forecast")
    st.write(f"Selected Stock: **{symbol}**")

    result = forecast_pipeline(symbol)

    current_price = result["current_price"]
    predicted_price = result["predicted_price"]
    actual_prices = result["actual_prices"]
    predictions = result["predictions"]
    
    # Instead of showing all the points and make the graph crowded we take last 100 points Only
    actual_prices = actual_prices[-100:]
    predictions = predictions[-100:]

    expected_return = ((predicted_price - current_price)/ current_price) * 100

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Current Price",f"${current_price:.2f}",)

    with col2:
        st.metric("Predicted Price",f"${predicted_price:.2f}",)

    with col3:
        st.metric("Expected Return",f"{expected_return:.2f}%",)

    st.markdown("---")
    
    plot(symbol,actual_prices,predictions)

    if expected_return > 0:
        st.success("📈 Bullish Forecast")
    else:
        st.error("📉 Bearish Forecast")
    
