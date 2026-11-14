from app.data_pipeline.logger import logger

from app.rag.config import TOP_K, MAX_DISTANCE
from app.rag.vector_store import get_vector_store


def create_retriever():
    """
    Create a LangChain retriever from the (cached) vector store.
    """
    return get_vector_store().as_retriever(search_kwargs={"k": TOP_K})


def retrieve_documents(query: str, top_k: int = TOP_K, max_distance: float = MAX_DISTANCE):
    """
    Retrieve the most relevant chunks for a query.

    Chunks that are too far from the question are dropped, so the assistant
    answers "I don't have enough information" instead of using unrelated text.
    Each returned document has its distance in metadata["distance"].
    """
    logger.info(f"Searching for: {query}")

    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(query, k=top_k)

    documents = []
    seen = set()

    for doc, distance in results:

        if float(distance) > max_distance:
            continue

        if doc.page_content in seen:      # overlapping chunks can repeat
            continue
        seen.add(doc.page_content)

        doc.metadata["distance"] = round(float(distance), 3)
        documents.append(doc)

    logger.info(f"{len(documents)} relevant documents retrieved.")

    return documents


# This is only for testing purposes
if __name__ == "__main__":

    query = "Should I buy Apple stock?"

    documents = retrieve_documents(query)

    print()

    for i, doc in enumerate(documents, start=1):

        print(f"Document {i}")
        print("-" * 40)
        print(doc.page_content)
        print(doc.metadata)
        print()