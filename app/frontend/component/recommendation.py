import streamlit as st

from app.recommendation.pipeline import recommendation_pipeline


def show_recommendation(symbol: str):
    """
    Display AI investment recommendation.
    """

    st.header("🧠 AI Investment Recommendation")

    try:
        result = recommendation_pipeline(symbol)

        recommendation = result["recommendation"]
        confidence = result["confidence"]
        score = result["score"]
        reasons = result["reasons"]

        # Recommendation Box
        if recommendation == "Strong Buy":
            st.success(f"## {recommendation}")

        elif recommendation == "Buy":
            st.success(f"## {recommendation}")

        elif recommendation == "Hold":
            st.warning(f"## {recommendation}")

        elif recommendation == "Sell":
            st.error(f"## {recommendation}")

        else:
            st.error(f"## {recommendation}")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Confidence",f"{confidence:.1f}%")

        with col2:
            st.metric("Score",f"{score:.2f}")

        st.subheader("Why?")

        for reason in reasons:
            st.write(f"✅ {reason}")

    except Exception as e:
        st.error(f"Recommendation Error: {e}")
    
 