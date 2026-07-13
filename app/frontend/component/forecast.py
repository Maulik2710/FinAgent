import streamlit as st


def show_forecast(symbol: str):
    """
    Display the forecast page.
    """

    st.header("📈 Stock Price Forecast")
    st.write(f"Selected Stock: **{symbol}**")

    # Placeholder values (we'll replace these with real ones)
    current_price = 220.15
    predicted_price = 245.30

    expected_return = ((predicted_price - current_price)/ current_price) * 100

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Current Price",f"${current_price:.2f}",)

    with col2:
        st.metric("Predicted Price",f"${predicted_price:.2f}",)

    with col3:
        st.metric("Expected Return",f"{expected_return:.2f}%",)

    st.markdown("---")

    if expected_return > 0:
        st.success("📈 Bullish Forecast")
    else:
        st.error("📉 Bearish Forecast")