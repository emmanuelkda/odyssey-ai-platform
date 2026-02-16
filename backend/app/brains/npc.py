# backend/app/brains/npc.py

from backend.app.llm import ask_llm


NPC_SYSTEM_PROMPT = """
You are an excited Motown 25 audience member in 1983.
- You speak in short, natural sentences.
- You react to the show, the atmosphere, and the user.
- You stay in 1983 (no modern references, no phones, no internet).
- You don't invent impossible knowledge; you only react as a person in the crowd.
"""


def handle_npc(message: str) -> dict:
    prompt = (
        f"{NPC_SYSTEM_PROMPT}\n\n"
        f"User says to you: {message}\n"
        f"Answer as that audience member:"
    )
    text = ask_llm(prompt)

    return {
        "kind": "text",
        "speaker": "npc",
        "text": text,
    }
