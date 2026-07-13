import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    
import streamlit as st
from app.frontend.component.forecast import show_forecast
from app.frontend.component.recommendation import show_recommendation

# Page Configuration
st.set_page_config(
    page_title="FinAgent",
    page_icon="📈",
    layout="wide",
)

# Sidebar

st.sidebar.title("FinAgent")

st.sidebar.markdown("### AI Financial Assistant")

selected_stock = st.sidebar.selectbox(
    "Select Stock",
    [
        "AAPL",
        "MSFT",
        "NVDA",
        "GOOGL",
        "AMZN",
        "META",
        "TSLA",
        "AMD",
        "NFLX",
        "JPM",
    ],
)
show_forecast(selected_stock)

st.divider()

show_recommendation(selected_stock)

st.sidebar.markdown("---")

st.sidebar.info(
    f"Currently Selected:\n\n**{selected_stock}**"
)

# Main Title
st.title("FinAgent")

st.caption(
    "AI-Powered Financial Forecasting, Portfolio Optimization, "
    "News Sentiment Analysis and RAG Assistant"
)

st.markdown("---")

# Tabs
forecast_tab, portfolio_tab, news_tab, recommendation_tab, chatbot_tab = st.tabs(
    [
        "📈 Forecast",
        "💼 Portfolio",
        "📰 News",
        "⭐ Recommendation",
        "🤴 AI Assistant",
    ]
)

# Forecast
with forecast_tab:
    show_forecast(selected_stock)

# Portfolio
with portfolio_tab:

    st.header("Portfolio Optimization")
    st.info("Portfolio optimization results will appear here.")

# News
with news_tab:

    st.header("News Sentiment")
    st.info("News sentiment analysis will appear here.")

# Recommendation
with recommendation_tab:

    st.header("Recommendation")
    st.info("Recommendation engine output will appear here.")

# AI Chat
with chatbot_tab:

    st.header("AI Financial Assistant")
    st.info("Chat with FinAgent using RAG + Gemini.")