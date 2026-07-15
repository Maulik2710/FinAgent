from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY is None:
    raise ValueError(
        "GEMINI_API_KEY not found in .env file."
    )
LLM_MODEL = "gemini-2.5-flash"

# Embedding model
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Gemini model
LLM_MODEL = "gemini-2.5-flash"

# Text splitter
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# Number of retrieved documents
TOP_K = 4

# Data directories
KNOWLEDGE_DIR = Path("data/knowledge")
KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)

NEWS_DIR = Path("data/news/sentiment")
NEWS_DIR.mkdir(parents=True, exist_ok=True)

VECTOR_DB_DIR = Path("data/vector_store")
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)