import streamlit as st

from app.rag.chain import ask_question


def show_chatbot():

    st.header("🤖 AI Financial Assistant")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User input
    question = st.chat_input("Ask me anything about investing...")

    if question:

        # Display user message
        with st.chat_message("user"):
            st.write(question)

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        # Generate answer
        with st.spinner("Thinking..."):
            answer = ask_question(question)

        # Display assistant message
        with st.chat_message("assistant"):
            st.write(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )