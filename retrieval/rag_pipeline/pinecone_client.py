import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

import os
from pinecone import Pinecone
from dotenv import load_dotenv
from pathlib import Path

# -----------------------------
# LOAD .env FILE
# -----------------------------
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# -----------------------------
# READ ENV VARIABLES
# -----------------------------
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = "ats-rag"

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY environment variable not set")

# -----------------------------
# INITIALIZE PINECONE
# -----------------------------
pc = Pinecone(api_key=PINECONE_API_KEY)

# -----------------------------
# CONNECT TO INDEX
# -----------------------------
if INDEX_NAME not in pc.list_indexes().names():
    raise ValueError(
        f"Pinecone index '{INDEX_NAME}' does not exist. "
        f"Create it in Pinecone dashboard first."
    )

index = pc.Index(INDEX_NAME)
