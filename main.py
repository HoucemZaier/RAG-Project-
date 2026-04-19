"""Point d'entrée du projet RAG - Orchestration complète"""

import sys
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ingestion import ingest_all_documents
from retrieval import interactive_rag
from config import DATA_DIR


def main():
    """Pipeline principal"""
    print("=" * 50)
    print("🤖 Système RAG - Orchestration")
    print("=" * 50)
    
    # Vérifier que des documents existent
    doc_files = list(DATA_DIR.glob("*.pdf")) + list(DATA_DIR.glob("*.txt"))
    
    if not doc_files:
        print(f"\n⚠️  Aucun document trouvé dans {DATA_DIR}")
        print("📌 Placez vos fichiers PDF ou TXT dans le dossier 'data/'")
        return
    
    # Phase 1: Ingestion
    print("\n" + "=" * 50)
    print("Phase 1: INGESTION DES DOCUMENTS")
    print("=" * 50)
    ingest_all_documents()
    
    # Phase 2: Interrogation RAG
    print("\n" + "=" * 50)
    print("Phase 2: INTERROGATION RAG")
    print("=" * 50)
    interactive_rag()


if __name__ == "__main__":
    main()
