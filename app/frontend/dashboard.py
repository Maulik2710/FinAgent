import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
    
import streamlit as st
from app.frontend.component.forecast import show_forecast
from app.frontend.component.recommendation import show_recommendation
from app.frontend.component.news import show_news
from app.frontend.component.portfolio import show_portfolio
from app.frontend.component.chatbot import show_chatbot

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
refresh = st.sidebar.button("🔄 Refresh")

st.divider()

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
    show_portfolio()

# News
with news_tab:
    show_news(selected_stock)

# Recommendation
with recommendation_tab:
    show_recommendation(selected_stock)

# AI Chat
with chatbot_tab:
    show_chatbot()