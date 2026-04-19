"""Phase 2: Pipeline RAG (Retrieval-Augmented Generation)"""

from pathlib import Path
from typing import List, Tuple
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from config import CHROMA_DB_PATH, COLLECTION_NAME, TOP_K_DOCUMENTS, EMBEDDING_MODEL, OLLAMA_MODEL, OLLAMA_BASE_URL

# Import optionnel pour l'évaluation
try:
    from ragas_eval import evaluate_response
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False


def load_vector_db(db_path: Path = CHROMA_DB_PATH) -> Chroma:
    """
    Charge la base de données Chroma
    
    Args:
        db_path: Chemin de la base de données Chroma
    
    Returns:
        Instance Chroma DB
    """
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    
    vector_db = Chroma(
        persist_directory=str(db_path),
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME
    )
    
    return vector_db


def create_answer_from_context(question: str, context: str, llm: OllamaLLM) -> str:
    """
    Crée une réponse pertinente en utilisant Ollama LLM avec un meilleur prompt
    
    Args:
        question: La question posée
        context: Le contexte extrait des documents
        llm: Instance OllamaLLM
    
    Returns:
        Une réponse générée par le LLM
    """
    if not context.strip():
        return "Je n'ai trouvé aucune information pertinente dans les documents pour répondre à cette question."
    
    # Meilleur prompt qui force une synthèse structurée
    prompt = f"""Tu es un assistant expert. Réponds UNIQUEMENT à partir du contexte fourni.

RÈGLES IMPORTANTES:
1. Synthétise les informations au lieu de les énumérer
2. Donne une réponse claire et structurée
3. Utilise des points clés numérotés si nécessaire
4. Ne mentionne JAMAIS les "chunks" ou l'architecture interne
5. Si c'est un processus, explique les ÉTAPES (Étape 1, Étape 2, etc.)
6. Sois concis mais complet
7. Réponds en français

CONTEXTE DES DOCUMENTS:
{context}

QUESTION: {question}

Réponds maintenant de manière claire et structurée:"""
    
    try:
        # Appeler Ollama pour générer la réponse
        answer = llm.invoke(prompt)
        return answer.strip()
    except Exception as e:
        print(f"Erreur Ollama: {e}")
        return f"Erreur lors de la génération: {str(e)}"


def query_rag(question: str, vector_db: Chroma, llm: OllamaLLM) -> Tuple[str, List[str]]:
    """
    Pose une question au système RAG avec génération par Ollama
    
    Args:
        question: La question à poser
        vector_db: La base de données vectorielle
        llm: Instance OllamaLLM
    
    Returns:
        Tuple contenant la réponse et les documents sources
    """
    try:
        # Créer le retriever
        retriever = vector_db.as_retriever(
            search_kwargs={"k": TOP_K_DOCUMENTS}
        )
        
        # Récupérer les documents pertinents
        docs = retriever.invoke(question)
        
        if not docs:
            return "Aucun document pertinent trouvé pour votre question.", []
        
        # Créer le contexte
        context = "\n\n".join([doc.page_content for doc in docs])
        
        # Générer la réponse avec Ollama
        answer = create_answer_from_context(question, context, llm)
        
        # Extraire les sources - gérer les métadonnées correctement
        sources = []
        for doc in docs:
            if hasattr(doc, 'metadata') and doc.metadata:
                source = doc.metadata.get("source", "Document inconnu")
            else:
                source = "Document inconnu"
            if source not in sources:  # Éviter les doublons
                sources.append(source)
        
        return answer, sources
    except Exception as e:
        import traceback
        print(f"Erreur détaillée: {traceback.format_exc()}")
        return f"Erreur lors du traitement: {str(e)}", []


def interactive_rag():
    """Mode interactif pour interroger le RAG avec Ollama et évaluation optionnelle"""
    print("🚀 Chargement du système RAG...")
    
    # Initialiser le LLM Ollama
    print("🤖 Connexion à Ollama...")
    try:
        llm = OllamaLLM(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.7
        )
        print(f"✓ Ollama ({OLLAMA_MODEL}) connecté!")
    except Exception as e:
        print(f"❌ Erreur de connexion à Ollama: {e}")
        print(f"   Assurez-vous que Ollama est en cours d'exécution")
        return
    
    # Charger la base de données vectorielle
    vector_db = load_vector_db()
    print("✓ Base de données vectorielle chargée!")
    
    # Demander si l'utilisateur veut l'évaluation RAGAS
    enable_eval = False
    if RAGAS_AVAILABLE:
        print("\n💡 Évaluation RAGAS disponible!")
        choice = input("Voulez-vous activer l'évaluation RAGAS? (o/n): ").strip().lower()
        enable_eval = choice in ['o', 'oui', 'yes', 'y']
        if enable_eval:
            print("✅ Évaluation RAGAS activée (ralentira légèrement les réponses)")
    
    print("\n💬 Mode interactif (tapez 'quit' pour quitter):\n")
    
    while True:
        question = input("Votre question: ").strip()
        
        if question.lower() == "quit":
            print("Au revoir! 👋")
            break
        
        if not question:
            continue
        
        print("\n⏳ Recherche et génération en cours...")
        answer, sources = query_rag(question, vector_db, llm)
        
        print(f"\n🤖 Réponse:\n{answer}\n")
        print(f"📚 Sources: {', '.join(sources) if sources else 'Aucune'}\n")
        
        # Évaluation optionnelle
        if enable_eval and RAGAS_AVAILABLE:
            try:
                # Récupérer le contexte pour l'évaluation
                retriever = vector_db.as_retriever(search_kwargs={"k": TOP_K_DOCUMENTS})
                docs = retriever.invoke(question)
                context = "\n\n".join([doc.page_content for doc in docs])
                
                evaluate_response(question, answer, context, sources)
            except Exception as e:
                print(f"⚠️ Erreur évaluation: {e}\n")
        
        print("-" * 60 + "\n")


if __name__ == "__main__":
    interactive_rag()
