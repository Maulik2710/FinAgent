import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from app.portfolio.pipeline import portfolio_optimization_pipeline


def show_portfolio():

    st.header("💼 Portfolio Optimization")

    result = portfolio_optimization_pipeline()

    symbols = result["symbols"]
    weights = result["weights"]
    portfolio_return = result["return"]
    volatility = result["volatility"]
    sharpe = result["sharpe"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Expected Return", f"{portfolio_return:.2%}")

    with col2:
        st.metric("Volatility", f"{volatility:.2%}")

    with col3:
        st.metric("Sharpe Ratio", f"{sharpe:.2f}")

    st.markdown("---")
    
    portfolio_df = pd.DataFrame({
        "Stock": symbols,
        "Allocation": weights * 100,
    })
    
    portfolio_df = portfolio_df.sort_values("Allocation",ascending=False,)
    
    # remove allocations below 1%:
    portfolio_df = portfolio_df[portfolio_df["Allocation"] > 1]

    st.subheader("Portfolio Allocation")

    st.dataframe(
        portfolio_df,
        use_container_width=True,
        hide_index=True,
    )
    
    fig, ax = plt.subplots(figsize=(6,6))

    ax.pie(
        portfolio_df["Allocation"],
        labels=portfolio_df["Stock"],
        autopct="%1.1f%%",
        startangle=90,
    )

    ax.set_title("Optimal Portfolio Allocation")

    st.pyplot(fig)