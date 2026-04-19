"""Évaluation des réponses RAG avec RAGAS"""

from typing import List, Dict
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from config import RAGAS_METRICS


def create_evaluation_dataset(
    questions: List[str],
    answers: List[str],
    contexts: List[List[str]],
    ground_truths: List[str]
) -> Dataset:
    """
    Crée un dataset pour l'évaluation RAGAS
    
    Args:
        questions: Liste des questions
        answers: Liste des réponses générées
        contexts: Liste des contextes pour chaque question
        ground_truths: Liste des réponses attendues
    
    Returns:
        Dataset formaté pour RAGAS
    """
    eval_data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    
    return Dataset.from_dict(eval_data)


def evaluate_rag(dataset: Dataset) -> Dict:
    """
    Évalue le système RAG avec les métriques RAGAS
    
    Args:
        dataset: Dataset d'évaluation
    
    Returns:
        Résultats de l'évaluation
    """
    metrics = [
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    ]
    
    results = evaluate(dataset, metrics=metrics)
    
    return results


def print_evaluation_results(results: Dict):
    """
    Affiche les résultats de l'évaluation
    
    Args:
        results: Résultats de l'évaluation
    """
    print("\n📊 Résultats de l'évaluation RAGAS:\n")
    print(f"Faithfulness (Fidélité): {results['faithfulness']:.2%}")
    print(f"Answer Relevancy (Pertinence): {results['answer_relevancy']:.2%}")
    print(f"Context Precision (Précision du contexte): {results['context_precision']:.2%}")
    print(f"Context Recall (Rappel du contexte): {results['context_recall']:.2%}")
    
    avg_score = sum(results.values()) / len(results)
    print(f"\nScore moyen: {avg_score:.2%}")


if __name__ == "__main__":
    # Exemple d'utilisation
    questions = ["Question 1?", "Question 2?"]
    answers = ["Réponse 1", "Réponse 2"]
    contexts = [["Contexte 1"], ["Contexte 2"]]
    ground_truths = ["Vérité 1", "Vérité 2"]
    
    dataset = create_evaluation_dataset(questions, answers, contexts, ground_truths)
    results = evaluate_rag(dataset)
    print_evaluation_results(results)
