import pandas as pd

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.data_pipeline.logger import logger

from app.rag.config import (
    KNOWLEDGE_DIR,
    KNOWLEDGE_EXTENSIONS,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    NEWS_DIR,
)


def _clean(value) -> str:
    """Return a clean string ('' for NaN / None)."""
    if value is None or pd.isna(value):
        return ""
    return str(value).strip()


def load_knowledge_documents() -> list:
    """
    Load all .txt / .md files from the knowledge directory (UTF-8).
    """
    documents = []

    for path in sorted(KNOWLEDGE_DIR.glob("*")):

        if path.suffix.lower() not in KNOWLEDGE_EXTENSIONS:
            continue

        text = path.read_text(encoding="utf-8", errors="ignore").strip()

        if not text:
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={"source": path.name, "type": "knowledge"},
            )
        )

    return documents


def load_news_documents() -> list:
    """
    Turn every saved news article (with its sentiment) into one document.

    Each document names the stock and date inside the text, so questions like
    "what is the news on Tesla?" can find it, and the metadata keeps the symbol.
    """
    documents = []

    for path in sorted(NEWS_DIR.glob("*.csv")):

        symbol = path.stem.upper()

        try:
            news_df = pd.read_csv(path)
        except Exception as e:
            logger.warning(f"Could not read news file {path.name}: {e}")
            continue

        for _, row in news_df.iterrows():

            title = _clean(row.get("title"))

            if not title:
                continue

            description = _clean(row.get("description"))
            publisher = _clean(row.get("source"))
            published = _clean(row.get("publishedAt"))[:10]
            sentiment = _clean(row.get("sentiment")) or "unknown"
            url = _clean(row.get("url"))

            try:
                confidence = f"{float(row.get('confidence')):.0%}"
            except (TypeError, ValueError):
                confidence = "n/a"

            content = (
                f"News about {symbol} ({published}, {publisher}): {title}. "
                f"{description} "
                f"Sentiment: {sentiment} (confidence {confidence})."
            )

            documents.append(
                Document(
                    page_content=content,
                    metadata={
                        "source": f"{symbol} news",
                        "type": "news",
                        "symbol": symbol,
                        "published": published,
                        "url": url,
                    },
                )
            )

    return documents


def load_documents() -> list:
    """
    Load knowledge documents and saved news.
    """
    logger.info("Loading knowledge documents...")

    knowledge = load_knowledge_documents()
    news = load_news_documents()

    documents = knowledge + news

    logger.info(
        f"{len(documents)} documents loaded "
        f"({len(knowledge)} knowledge, {len(news)} news)."
    )

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
    Load and split all documents.
    """
    documents = load_documents()

    return split_documents(documents)


# This is only for testing purposes
if __name__ == "__main__":

    chunks = load_and_split_documents()
    print(f"Total Chunks: {len(chunks)}\n")

    if chunks:
        print(chunks[0])
    else:
        print("No documents found. Add .txt files to data/knowledge.")