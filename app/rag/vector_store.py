from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from app.data_pipeline.logger import logger

from app.rag.config import (
    EMBEDDING_MODEL,
    VECTOR_DB_DIR,
)

from app.rag.loader import load_and_split_documents


def load_embedding_model():
    """
    Load the embedding model.
    """

    logger.info("Loading embedding model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    return embeddings

def create_vector_store():
    """
    Create a FAISS vector store from the knowledge base.
    """

    logger.info("Creating vector store...")

    documents = load_and_split_documents()

    embeddings = load_embedding_model()

    vector_store = FAISS.from_documents(
        documents,
        embeddings,
    )

    logger.info("Vector store created successfully.")

    return vector_store

def save_vector_store(vector_store):
    """
    Save the FAISS vector store.
    """

    logger.info("Saving vector store...")

    vector_store.save_local(
        str(VECTOR_DB_DIR)
    )

    logger.info("Vector store saved successfully.")
    
    
def load_vector_store():
    """
    Load the saved FAISS vector store.
    """

    logger.info("Loading vector store...")

    embeddings = load_embedding_model()

    vector_store = FAISS.load_local(
        str(VECTOR_DB_DIR),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    logger.info("Vector store loaded successfully.")

    return vector_store


# This is Only for the Testing Purpose
if __name__ == "__main__":

    vector_store = create_vector_store()
    save_vector_store(vector_store)
    vector_store = load_vector_store()
    print(vector_store.index.ntotal)