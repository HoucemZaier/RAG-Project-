"""Phase 1: Indexation des documents (Document Ingestion)"""

from pathlib import Path
from typing import List, Dict, Tuple
import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from config import DATA_DIR, CHROMA_DB_PATH, COLLECTION_NAME, CHUNK_SIZE, CHUNK_OVERLAP, EMBEDDING_MODEL


def load_documents(data_dir: Path = DATA_DIR) -> List[Tuple[str, str]]:
    """
    Charge tous les documents (PDF et TXT) depuis le répertoire data/
    Retourne une liste de tuples (contenu, nom_fichier)
    
    Args:
        data_dir: Chemin du répertoire contenant les documents
    
    Returns:
        Liste de tuples (contenu, source)
    """
    documents = []
    
    # Charger les fichiers PDF
    for pdf_file in data_dir.glob("*.pdf"):
        try:
            with open(pdf_file, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                if text.strip():
                    documents.append((text, pdf_file.name))
        except Exception as e:
            print(f"  ⚠️ Erreur PDF {pdf_file.name}: {e}")
    
    # Charger les fichiers TXT
    for txt_file in data_dir.glob("*.txt"):
        try:
            with open(txt_file, "r", encoding="utf-8") as f:
                content = f.read()
                if content.strip():
                    documents.append((content, txt_file.name))
        except Exception as e:
            print(f"  ⚠️ Erreur TXT {txt_file.name}: {e}")
    
    return documents


def chunk_documents(documents: List[Tuple[str, str]], chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[Document]:
    """
    Divise les documents en chunks avec métadonnées
    
    Args:
        documents: Liste des tuples (contenu, source)
        chunk_size: Taille de chaque chunk
        chunk_overlap: Chevauchement entre les chunks
    
    Returns:
        Liste des Document objects avec métadonnées
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunk_docs = []
    for doc_content, source in documents:
        if not doc_content.strip():
            continue
            
        # Diviser le texte
        text_chunks = splitter.split_text(doc_content)
        
        # Créer des Document objects avec métadonnées
        for i, chunk in enumerate(text_chunks):
            if chunk.strip():  # Ignorer les chunks vides
                doc = Document(
                    page_content=chunk,
                    metadata={"source": source, "chunk_index": i}
                )
                chunk_docs.append(doc)
    
    return chunk_docs


def index_documents(chunk_docs: List[Document], db_path: Path = CHROMA_DB_PATH) -> Chroma:
    """
    Indexe les chunks dans Chroma DB avec métadonnées
    
    Args:
        chunk_docs: Liste des Document objects à indexer
        db_path: Chemin de la base de données Chroma
    
    Returns:
        Instance Chroma DB
    """
    if not chunk_docs:
        raise ValueError("Aucun document à indexer!")
    
    print(f"  📝 Documents à indexer: {len(chunk_docs)} chunks")
    
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    # Utiliser from_documents pour préserver les métadonnées
    try:
        vector_db = Chroma.from_documents(
            documents=chunk_docs,
            embedding=embeddings,
            persist_directory=str(db_path),
            collection_name=COLLECTION_NAME
        )
    except Exception as e:
        print(f"  ❌ Erreur Chroma: {e}")
        raise
    
    return vector_db


def ingest_all_documents():
    """Pipeline d'ingestion complète"""
    print("📥 Phase 1: Chargement des documents...")
    documents = load_documents()
    
    if not documents:
        print("⚠️  Aucun document trouvé!")
        return None
    
    print(f"✓ {len(documents)} document(s) chargé(s)\n")
    
    print("✂️ Chunking des documents...")
    chunks = chunk_documents(documents)
    print(f"✓ {len(chunks)} chunk(s) créé(s)\n")
    
    if not chunks:
        print("⚠️  Aucun chunk créé!")
        return None
    
    print("📊 Indexation dans Chroma DB...")
    try:
        vector_db = index_documents(chunks)
        print("✓ Indexation complète\n")
    except Exception as e:
        print(f"❌ Erreur lors de l'indexation: {e}")
        return None
    
    return vector_db


if __name__ == "__main__":
    ingest_all_documents()
