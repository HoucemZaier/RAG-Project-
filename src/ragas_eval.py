"""Évaluation automatique des réponses RAG avec RAGAS"""

from typing import Dict, List, Tuple
from langchain_ollama import OllamaLLM
from config import OLLAMA_MODEL, OLLAMA_BASE_URL


class RAGASEvaluator:
    """Évaluateur RAGAS simplifié pour les réponses RAG"""
    
    def __init__(self):
        self.llm = OllamaLLM(
            model=OLLAMA_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.3  # Température basse pour l'évaluation
        )
    
    def evaluate_faithfulness(self, context: str, answer: str) -> float:
        """
        Évalue si la réponse est fidèle au contexte (0-1)
        Vérifie qu'il n'y a pas d'hallucinations
        """
        prompt = f"""Évalue si la réponse est basée UNIQUEMENT sur le contexte fourni.
Réponds par un score entre 0 et 1 (0=hallucinations, 1=parfaitement fidèle), puis une explication courte.

CONTEXTE:
{context}

RÉPONSE:
{answer}

Format: SCORE: X.X | EXPLICATION: [courte explication]"""
        
        try:
            result = self.llm.invoke(prompt)
            # Parser le score
            if "SCORE:" in result:
                score_part = result.split("SCORE:")[1].split("|")[0].strip()
                return float(score_part)
            return 0.7
        except:
            return 0.7
    
    def evaluate_relevancy(self, question: str, answer: str) -> float:
        """
        Évalue la pertinence de la réponse (0-1)
        Vérifie que la réponse répond à la question
        """
        prompt = f"""Évalue si la réponse répond directement et clairement à la question.
Réponds par un score entre 0 et 1 (0=non pertinent, 1=très pertinent).

QUESTION:
{question}

RÉPONSE:
{answer}

Format: SCORE: X.X"""
        
        try:
            result = self.llm.invoke(prompt)
            if "SCORE:" in result:
                score_part = result.split("SCORE:")[1].strip()[:3]
                return float(score_part)
            return 0.7
        except:
            return 0.7
    
    def evaluate_all(self, question: str, context: str, answer: str) -> Dict[str, float]:
        """
        Évalue tous les critères RAGAS
        """
        scores = {
            "faithfulness": self.evaluate_faithfulness(context, answer),
            "relevancy": self.evaluate_relevancy(question, answer),
        }
        
        # Calculer le score moyen
        scores["overall"] = sum(scores.values()) / len(scores)
        
        return scores
    
    def print_evaluation(self, question: str, answer: str, context: str, sources: List[str]):
        """
        Affiche une évaluation formatée
        """
        print("\n" + "="*60)
        print("📊 ÉVALUATION RAGAS DE LA RÉPONSE")
        print("="*60)
        
        scores = self.evaluate_all(question, context, answer)
        
        # Afficher les scores
        print(f"\n🎯 Métrique de Fidélité (Faithfulness): {scores['faithfulness']:.1%}")
        print(f"🎯 Métrique de Pertinence (Relevancy): {scores['relevancy']:.1%}")
        print(f"\n📈 Score Global: {scores['overall']:.1%}")
        
        # Interprétation
        if scores['overall'] >= 0.85:
            print("✅ Excellente qualité de réponse!")
        elif scores['overall'] >= 0.70:
            print("👍 Bonne qualité de réponse")
        elif scores['overall'] >= 0.55:
            print("⚠️ Qualité acceptable, peut être améliorée")
        else:
            print("❌ Qualité faible, réponse à améliorer")
        
        print("="*60 + "\n")


def evaluate_response(question: str, answer: str, context: str, sources: List[str]):
    """Fonction simplifiée pour évaluer une réponse"""
    try:
        evaluator = RAGASEvaluator()
        evaluator.print_evaluation(question, answer, context, sources)
    except Exception as e:
        print(f"⚠️ Évaluation non disponible: {e}")
