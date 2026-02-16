# backend/app/brains/smalltalk.py

from backend.app.llm import ask_llm


SMALLTALK_PROMPT = """
You are a friendly guide inside a Motown 25 simulation experience.
Keep responses light, warm, and brief.
If the user references the show, you can react to it.
"""


def handle_smalltalk(message: str) -> dict:
    prompt = (
        f"{SMALLTALK_PROMPT}\n\n"
        f"User: {message}\n"
        f"Guide:"
    )
    text = ask_llm(prompt)

    return {
        "kind": "text",
        "speaker": "guide",
        "text": text,
    }
