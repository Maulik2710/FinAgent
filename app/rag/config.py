import os

from dotenv import load_dotenv

from app.data_pipeline.config import PROJECT_ROOT, DATA_DIR, NEWS_DATA_DIR

# Load the .env file (project root first, then the app/ folder, then default lookup)
load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(PROJECT_ROOT / "app" / ".env")
load_dotenv()

# ----------------------------
# Gemini
# ----------------------------
# The key is checked when the LLM is actually loaded (chain.load_llm), NOT here,
# so building the vector store / testing retrieval works without a key.
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

LLM_MODEL = "gemini-2.5-flash"
LLM_TEMPERATURE = 0.2

# ----------------------------
# Embedding model
# ----------------------------
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ----------------------------
# Text splitter
# ----------------------------
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# ----------------------------
# Retrieval
# ----------------------------
# Number of retrieved chunks
TOP_K = 4

# Squared L2 distance on normalized embeddings: 0 = identical, 2 = opposite.
# 1.5 is roughly cosine similarity 0.25. Chunks farther away than this are
# treated as irrelevant. Lower it for stricter answers, raise it if the
# assistant says "I don't have enough information" too often.
MAX_DISTANCE = 1.5

# Number of previous chat turns given to the model for follow-up questions
MAX_HISTORY_TURNS = 4

# ----------------------------
# Data directories (absolute paths, same as the rest of the project)
# ----------------------------
KNOWLEDGE_DIR = DATA_DIR / "knowledge"
KNOWLEDGE_EXTENSIONS = {".txt", ".md"}

NEWS_DIR = NEWS_DATA_DIR / "sentiment"

VECTOR_DB_DIR = DATA_DIR / "vector_store"

KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
NEWS_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)