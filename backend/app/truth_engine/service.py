from __future__ import annotations

from typing import Any, Dict

from backend.app.truth_engine.retriever import search_facts


def answer_question(question: str) -> Dict[str, Any]:
    """
    Stable Truth Engine entrypoint for the flagship repo.
    """
    result = search_facts(question)

    if isinstance(result, dict):
        return result

    return {"answer": str(result)}
