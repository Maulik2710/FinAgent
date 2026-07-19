import streamlit as st
from app.news.pipeline import news_sentiment_pipeline


def show_news(symbol: str):

    st.header("📰 Latest Financial News")

    try:
        result = news_sentiment_pipeline(symbol)
        
        overall_sentiment = "NEUTRAL"
        sentiment_score = result["score"]
        if sentiment_score >= 0.2:
            overall_sentiment = "POSITIVE"
        
        if sentiment_score <= -0.2:
            overall_sentiment = "NEGATIVE"
        
        articles = result["news"]

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Overall Sentiment: ", overall_sentiment)

        with col2:
            st.metric("Sentiment Score: ", f"{sentiment_score:.2f}")

        st.markdown("---")

        for article in articles:

            with st.expander(f"📰 {article['title']}"):
                st.write(article["description"])

                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**Source:** {article['source']}")

                with col2:
                    st.write(f"**Published:** {article['publishedAt'][:10]}")

                st.write(f"**Sentiment:** {article['sentiment'].title()}")
                st.write(f"**Confidence:** {article['confidence']:.2f}")

                st.link_button("Read Full Article", article["url"])

    except Exception as e:
        st.error(e)