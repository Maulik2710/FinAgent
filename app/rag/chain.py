from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.rag.config import (
    GEMINI_API_KEY,
    LLM_MODEL,
)

from app.rag.retriever import retrieve_documents
from app.data_pipeline.logger import logger


def load_llm():
    """
    Load Gemini.
    """

    logger.info("Loading Gemini...")

    return ChatGoogleGenerativeAI(
        model=LLM_MODEL,
        google_api_key=GEMINI_API_KEY,
        temperature=0.2,
    )


def build_prompt():
    """
    Build the financial assistant prompt.
    """

    return ChatPromptTemplate.from_template(
        """
You are FinAgent, an AI Financial Assistant.

You MUST answer ONLY using the provided context.

If the answer is not contained in the context, respond exactly:

"I don't have enough information in my knowledge base to answer that."

Do not use your own knowledge.
Do not make assumptions.
Do not invent facts.

Context:
{context}

Question:
{question}

Answer:
"""
    )


def ask_question(question: str):
    """
    Answer a question using retrieved context.
    """

    logger.info("Retrieving documents...")
    docs = retrieve_documents(question)
    context = "\n\n".join(
        f"Source: {doc.metadata['source']}\n{doc.page_content}"
        for doc in docs
    )
    llm = load_llm()
    prompt = build_prompt()
    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke(
        {
            "context": context,
            "question": question,
        }
    )

    return answer

# This is Only for the testing purpose
if __name__ == "__main__":

    response = ask_question(
        "Should I buy Apple stock?"
    )

    print(response)