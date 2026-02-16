# backend/app/brains/performance.py

from backend.app.llm import ask_llm


PERFORMANCE_PROMPT = """
You are an expert commentator on Michael Jackson's Billie Jean performance at Motown 25.
- Explain what makes the performance special: staging, timing, crowd reaction, choreography, vocals.
- Blend factual description with a bit of emotional color.
- Stay focused on this specific performance, not his entire career.
"""


def handle_performance_question(message: str) -> dict:
    prompt = (
        f"{PERFORMANCE_PROMPT}\n\n"
        f"Question: {message}\n"
        f"Answer:"
    )
    text = ask_llm(prompt)

    return {
        "kind": "text",
        "speaker": "analyst",
        "text": text,
    }
