"""Configuration globale du projet RAG"""

import os
from pathlib import Path

# Chemins principaux
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_DIR = PROJECT_ROOT / "db"
SRC_DIR = PROJECT_ROOT / "src"

# Configuration Chroma DB
CHROMA_DB_PATH = DB_DIR / "chroma_db"
COLLECTION_NAME = "rag_documents"

# Configuration du modèle
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Configuration Ollama
OLLAMA_MODEL = "phi3:latest"  # Le modèle exact que vous avez téléchargé
OLLAMA_BASE_URL = "http://localhost:11434"  # URL par défaut d'Ollama

# Configuration RAG
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_DOCUMENTS = 3

# Configuration RAGAS (Evaluation)
RAGAS_METRICS = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]

# Créer les répertoires s'ils n'existent pas
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DB_PATH.mkdir(parents=True, exist_ok=True)
