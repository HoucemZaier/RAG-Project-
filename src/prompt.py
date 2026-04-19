"""Template de prompt pour le RAG"""

from langchain_core.prompts import PromptTemplate


def get_prompt_template() -> PromptTemplate:
    """
    Retourne le template de prompt optimisé pour RAG
    
    Returns:
        PromptTemplate configuré
    """
    template = """Utilisez les informations suivantes pour répondre à la question. 
Si vous ne connaissez pas la réponse, dites simplement que vous ne savez pas. 
Ne devinez pas et ne fournissez pas d'informations qui ne sont pas basées sur le contexte fourni.

Contexte:
{context}

Question: {question}

Réponse:"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
    
    return prompt


def get_evaluation_prompt() -> PromptTemplate:
    """
    Template de prompt pour l'évaluation RAGAS
    
    Returns:
        PromptTemplate pour l'évaluation
    """
    template = """Évaluez la qualité de la réponse suivante en fonction du contexte fourni.

Contexte: {context}
Question: {question}
Réponse: {answer}

Évaluation:"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question", "answer"]
    )
    
    return prompt
