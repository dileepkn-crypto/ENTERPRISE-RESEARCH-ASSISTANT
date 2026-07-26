import os
from pathlib import Path

from dotenv import load_dotenv


# ---------------------------------------------------------
# Project paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)


# ---------------------------------------------------------
# API configuration
# ---------------------------------------------------------


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

# ---------------------------------------------------------
# Embedding configuration
# ---------------------------------------------------------

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)


# ---------------------------------------------------------
# Storage paths
# ---------------------------------------------------------

CHROMA_PATH = BASE_DIR / os.getenv(
    "CHROMA_PATH",
    "data/chroma_db"
)

DATABASE_PATH = BASE_DIR / os.getenv(
    "DATABASE_PATH",
    "data/researchiq.db"
)

DOCUMENTS_PATH = BASE_DIR / "data" / "documents"


# ---------------------------------------------------------
# RAG configuration
# ---------------------------------------------------------

CHUNK_SIZE = int(
    os.getenv("CHUNK_SIZE", "800")
)

CHUNK_OVERLAP = int(
    os.getenv("CHUNK_OVERLAP", "120")
)

TOP_K = int(
    os.getenv("TOP_K", "5")
)


# ---------------------------------------------------------
# Create required directories
# ---------------------------------------------------------

CHROMA_PATH.mkdir(
    parents=True,
    exist_ok=True
)

DOCUMENTS_PATH.mkdir(
    parents=True,
    exist_ok=True
)