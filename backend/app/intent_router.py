# backend/app/intent_router.py

from enum import Enum
from openai import OpenAI
from backend.app.settings import settings


def get_client():
    return OpenAI(api_key=settings.OPENAI_API_KEY)


# ---------------------------------------------------------
# INTENT ENUM (updated with timeline-aware intents)
# ---------------------------------------------------------
class Intent(str, Enum):
    ASK_NPC = "ask_npc"
    ASK_HISTORICAL_QUESTION = "ask_historical_question"
    NAVIGATION = "navigation"
    SMALLTALK = "smalltalk"
    PERFORMANCE_QUESTION = "performance_question"
    SYSTEM_COMMAND = "system_command"
    UNKNOWN = "unknown"

    # NEW timeline-aware intents
    ASK_WHATS_HAPPENING_NOW = "ASK_WHATS_HAPPENING_NOW"
    ASK_WHATS_NEXT = "ASK_WHATS_NEXT"
    ASK_WHAT_JUST_HAPPENED = "ASK_WHAT_JUST_HAPPENED"
    ASK_SHOW_PROGRESS = "ASK_SHOW_PROGRESS"


# ---------------------------------------------------------
#  INTENT CLASSIFICATION PROMPT (with few-shot examples)
# ---------------------------------------------------------
INTENT_PROMPT = """
You are the Intent Router for the Odyssey Engine.

Classify the user's intent into ONE category:
- ask_historical_question
- ask_npc
- navigation
- performance_question
- system_command
- smalltalk
- unknown
- ASK_WHATS_HAPPENING_NOW
- ASK_WHATS_NEXT
- ASK_WHAT_JUST_HAPPENED
- ASK_SHOW_PROGRESS

Examples for ASK_WHATS_HAPPENING_NOW:
"What is happening right now?"
"Where are we in the show?"
"What part is this?"
"What’s going on right now?"
"What's happening on stage at this moment?"

Examples for ASK_WHATS_NEXT:
"What comes next?"
"What’s the next part of the show?"
"What's coming up after this?"

Examples for ASK_WHAT_JUST_HAPPENED:
"What just happened?"
"What was the last event?"
"What happened before this?"

Examples for ASK_SHOW_PROGRESS:
"How far into the show are we?"
"What time is it in the show now?"
"How long has the show been going?"

Return ONLY the intent name.
"""


# ---------------------------------------------------------
# CLASSIFY INTENT FUNCTION
# ---------------------------------------------------------
def classify_intent(message: str) -> Intent:
    """
    Sends the user message to OpenAI and extracts the normalized intent label.
    """

    client = get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": INTENT_PROMPT},
            {"role": "user", "content": message},
        ]
    )

    # Extract model output
    intent_str = response.choices[0].message.content.strip().lower()

    # Normalize formatting (spaces, hyphens)
    intent_str = response.choices[0].message.content.strip()
    intent_str = intent_str.replace(" ", "").replace("-", "_")


    # Map to Enum
    try:
        return Intent(intent_str)
    except ValueError:
        return Intent.UNKNOWN
