from langchain_community.document_loaders import DirectoryLoader, CSVLoader , TextLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.data_pipeline.logger import logger

from app.rag.config import (
    KNOWLEDGE_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    NEWS_DIR,
)

def load_documents():
    """
    Load all text documents from the knowledge directory.
    """

    logger.info("Loading knowledge documents...")

    loader1 = DirectoryLoader(
        path=str(KNOWLEDGE_DIR),
        glob="*.txt",
        loader_cls=TextLoader,
    )
    
    loader2 = DirectoryLoader(
        path=str(NEWS_DIR),
        glob="*.csv",
        loader_cls=CSVLoader,
    )

    documents1 = loader1.load()
    
    documents2 = loader2.load()
    
    documents = documents1 + documents2

    logger.info(f"{len(documents)} documents loaded.")

    return documents

def split_documents(documents):
    """
    Split documents into smaller chunks.
    """

    logger.info("Splitting documents...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    chunks = splitter.split_documents(documents)

    logger.info(f"{len(chunks)} chunks created.")

    return chunks

def load_and_split_documents():
    """
    Load and split all knowledge documents.
    """

    documents = load_documents()

    chunks = split_documents(documents)

    return chunks


# This is Only for the testing purpose
if __name__ == "__main__":

    chunks = load_and_split_documents()
    print(f"Total Chunks: {len(chunks)}")
    print()
    if chunks:
        print(f"Total Chunks: {len(chunks)}")
        print()
        print(chunks[0])
    else:
        print("No documents found in the knowledge directory.")