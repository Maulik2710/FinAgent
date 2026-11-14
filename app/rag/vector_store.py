import json
from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from app.data_pipeline.logger import logger

from app.rag.config import (
    EMBEDDING_MODEL,
    VECTOR_DB_DIR,
    KNOWLEDGE_DIR,
    KNOWLEDGE_EXTENSIONS,
    NEWS_DIR,
)

from app.rag.loader import load_and_split_documents

SIGNATURE_FILE = VECTOR_DB_DIR / "sources.json"
INDEX_FILE = VECTOR_DB_DIR / "index.faiss"

# In-memory copy of the loaded store, reused between questions
_cache = {"store": None, "signature": None}


@lru_cache(maxsize=1)
def load_embedding_model():
    """
    Load the embedding model (cached: loaded once per Python process).
    Embeddings are normalized so distances behave like cosine similarity.
    """
    logger.info("Loading embedding model...")

    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        encode_kwargs={"normalize_embeddings": True},
    )


def _source_signature() -> list:
    """
    A fingerprint of every file the vector store is built from
    (name, size, modified time). If it changes, the store is out of date.
    """
    files = [
        p for p in KNOWLEDGE_DIR.glob("*")
        if p.suffix.lower() in KNOWLEDGE_EXTENSIONS
    ]
    files += list(NEWS_DIR.glob("*.csv"))

    return sorted(
        [p.parent.name + "/" + p.name, p.stat().st_size, int(p.stat().st_mtime)]
        for p in files
    )


def vector_store_is_stale() -> bool:
    """
    True if the store does not exist yet, or the knowledge / news files
    changed since it was built.
    """
    if not INDEX_FILE.exists() or not SIGNATURE_FILE.exists():
        return True

    try:
        saved = json.loads(SIGNATURE_FILE.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return True

    return saved != _source_signature()


def create_vector_store():
    """
    Create a FAISS vector store from the knowledge base and saved news.
    """
    logger.info("Creating vector store...")

    chunks = load_and_split_documents()

    if not chunks:
        raise ValueError(
            "No documents found. Add .txt or .md files to data/knowledge "
            "(or download news) before building the vector store."
        )

    vector_store = FAISS.from_documents(chunks, load_embedding_model())

    logger.info(f"Vector store created successfully ({len(chunks)} chunks).")

    return vector_store


def save_vector_store(vector_store) -> None:
    """
    Save the FAISS vector store and the fingerprint of its source files.
    """
    logger.info("Saving vector store...")

    vector_store.save_local(str(VECTOR_DB_DIR))

    SIGNATURE_FILE.write_text(
        json.dumps(_source_signature()), encoding="utf-8"
    )

    logger.info("Vector store saved successfully.")


def load_vector_store():
    """
    Load the saved FAISS vector store.
    """
    if not INDEX_FILE.exists():
        raise FileNotFoundError(
            "Vector store not found. Run: python -m app.rag.vector_store"
        )

    logger.info("Loading vector store...")

    # allow_dangerous_deserialization is needed by FAISS; it is safe here
    # because we only load a file that this project created itself.
    vector_store = FAISS.load_local(
        str(VECTOR_DB_DIR),
        load_embedding_model(),
        allow_dangerous_deserialization=True,
    )

    logger.info("Vector store loaded successfully.")

    return vector_store


def build_vector_store():
    """
    Build the store from the current files and save it.
    """
    vector_store = create_vector_store()
    save_vector_store(vector_store)

    _cache["store"] = vector_store
    _cache["signature"] = _source_signature()

    return vector_store


def get_vector_store(force_rebuild: bool = False):
    """
    Return a ready-to-use vector store.

    - Builds it automatically if it does not exist or the knowledge / news
      files changed (so fresh news is always searchable).
    - Keeps it in memory, so it is not reloaded for every question.
    """
    if force_rebuild or vector_store_is_stale():
        return build_vector_store()

    if _cache["store"] is None:
        _cache["store"] = load_vector_store()
        _cache["signature"] = _source_signature()

    return _cache["store"]


# Run this to (re)build the vector store from the command line
if __name__ == "__main__":

    store = build_vector_store()
    print(f"Vectors stored: {store.index.ntotal}")