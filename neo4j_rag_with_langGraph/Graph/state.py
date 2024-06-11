from typing import List, TypedDict


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        documents: result of chain
        article_ids: list of article id from vector search
        prompt: prompt template object
        prompt_with_context: prompt template with context from vector search
        subqueries: decomposed queries
    """

    question: str
    documents: dict
    article_ids: List[str]
    prompt: object
    prompt_with_context: object
    subqueries: object