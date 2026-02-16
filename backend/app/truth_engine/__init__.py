# backend/app/truth_engine/retriever.py

from typing import Optional, Dict, Any

from .facts import MOTOWN_25_FACTS


def search_facts(message: str) -> Optional[Dict[str, Any]]:
    """
    Very simple rule-based Truth Engine v1.

    Given a user message, try to map it to a known Motown 25 fact.
    Returns a structured dict if we find a match, otherwise None.
    """
    if not message:
        return None

    text = message.lower().strip()

    # --- LOCATION QUESTIONS ---
    # Examples:
    #   "Where is this happening?"
    #   "Where are we?"
    #   "Where is Motown 25?"
    if "where" in text and (
        "happening" in text
        or "are we" in text
        or "is this" in text
        or "motown 25" in text
        or "this event" in text
        or "here" in text
    ):
        return {
            "question_type": "location",
            "answer": f"This event is taking place at {MOTOWN_25_FACTS['location_full']}.",
            "fact_key": "location_full",
            "source": "motown_25_static_facts_v1",
        }

    # --- DATE QUESTIONS ---
    #   "When is this happening?"
    #   "When was Motown 25 recorded?"
    #   "What year is this?"
    if "when" in text and (
        "happening" in text
        or "this" in text
        or "motown 25" in text
        or "recorded" in text
    ):
        return {
            "question_type": "date",
            "answer": (
                f"This Motown 25 performance was recorded on "
                f"{MOTOWN_25_FACTS['recording_date']}."
            ),
            "fact_key": "recording_date",
            "source": "motown_25_static_facts_v1",
        }

    if "what year" in text or "what year is this" in text:
        return {
            "question_type": "year",
            "answer": "This Motown 25 performance took place in 1983.",
            "fact_key": "recording_date",
            "source": "motown_25_static_facts_v1",
        }

    # --- HOST QUESTIONS ---
    #   "Who is hosting Motown 25?"
    #   "Who is the host?"
    if ("who" in text and "host" in text) or "who's hosting" in text:
        return {
            "question_type": "host",
            "answer": (
                f"The host of Motown 25 is {MOTOWN_25_FACTS['host']}."
            ),
            "fact_key": "host",
            "source": "motown_25_static_facts_v1",
        }

    # --- GENERAL "WHAT IS THIS?" ---
    #   "What is this show?"
    #   "What is this event?"
    if "what is this" in text or "what's this" in text or "what is this show" in text:
        return {
            "question_type": "description",
            "answer": MOTOWN_25_FACTS["description"],
            "fact_key": "description",
            "source": "motown_25_static_facts_v1",
        }

    # No known fact yet
    return None
