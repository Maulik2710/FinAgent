from app.data_pipeline.logger import logger

from app.rag.config import TOP_K
from app.rag.vector_store import load_vector_store

def create_retriever():
    """
    Create a retriever from the FAISS vector store.
    """

    logger.info("Creating retriever...")
    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={"k": TOP_K}
    )

    logger.info("Retriever created successfully.")

    return retriever


def retrieve_documents(query: str):
    """
    Retrieve the most relevant documents for a query.
    """

    logger.info(f"Searching for: {query}")
    retriever = create_retriever()
    documents = retriever.invoke(query)

    logger.info(f"{len(documents)} documents retrieved.")

    return documents

# This is Only for the Testing purpose 
# if __name__ == "__main__":

#     query = "Should I buy Apple stock?"

#     documents = retrieve_documents(query)

#     print()

#     for i, doc in enumerate(documents, start=1):

#         print(f"Document {i}")
#         print("-" * 40)
#         print(doc.page_content)
#         print(doc.metadata)
#         print()