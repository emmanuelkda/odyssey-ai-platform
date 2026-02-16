# backend/app/truth_engine/retriever.py

import json
import os

# Load Motown 25 fact file
FACT_PATH = os.path.join(os.path.dirname(__file__), "motown25_facts.json")

with open(FACT_PATH, "r") as f:
    FACTS = json.load(f)


def search_facts(message: str):
    """
    Truth Engine v1.
    Returns a structured dict with:
        - question_type
        - answer
        - source

    Returns None if no match found.
    """

    msg = message.lower()

    # ========= LOCATION =========
    if "where" in msg or "location" in msg or "auditorium" in msg:
        return {
            "question_type": "location",
            "answer": FACTS["event"]["location"],
            "source": "motown25_facts_v1"
        }

    # ========= DATE =========
    if "when" in msg or "date" in msg:
        return {
            "question_type": "date",
            "answer": FACTS["event"]["date"],
            "source": "motown25_facts_v1"
        }

    # ========= AIR DATE =========
    if "air" in msg or "aired" in msg:
        return {
            "question_type": "aired_date",
            "answer": FACTS["event"]["aired_date"],
            "source": "motown25_facts_v1"
        }

    # ========= SONG MATCH =========
    for song in FACTS["songs"]:
        title = song["title"].lower()
        artist = song["performed_by"].lower()

        if title in msg or artist in msg:
            return {
                "question_type": "song_info",
                "answer": song,
                "source": "motown25_facts_v1"
            }

    # ========= WHO PERFORMED =========
    if "who performed" in msg or "performers" in msg or "setlist" in msg:
        return {
            "question_type": "performer_list",
            "answer": FACTS["songs"],  # full ordered list
            "source": "motown25_facts_v1"
        }

    # ========= PEOPLE / BIO QUESTIONS =========
    for person in FACTS.get("people", []):
        if person["name"].lower() in msg:
            return {
                "question_type": "person_info",
                "answer": person,
                "source": "motown25_facts_v1"
            }

    # No match found
    return None
