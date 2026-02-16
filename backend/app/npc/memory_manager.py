import json
import os

MEMORY_DIR = os.path.join(os.path.dirname(__file__), "npc_data")


def load_long_term_memory(npc_id: str):
    """Load or create long-term memory for an NPC."""
    path = os.path.join(MEMORY_DIR, f"{npc_id}.json")
    if not os.path.exists(path):
        return {
            "npc_id": npc_id,
            "traits": {
                "friendliness": 0.6,
                "excitement": 0.7,
                "sarcasm": 0.1,
                "talkativeness": 0.7
            },
            "bio": "An excited Motown 25 audience member.",
        }
    with open(path, "r") as f:
        return json.load(f)


def save_long_term_memory(npc_id: str, data: dict):
    """Persist updated long-term memory."""
    path = os.path.join(MEMORY_DIR, f"{npc_id}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_short_term_memory(npc_id: str):
    """Short-term memory persists only for the session."""
    path = os.path.join(MEMORY_DIR, f"{npc_id}_st_mem.json")
    if not os.path.exists(path):
        return {
            "recent_messages": [],
            "emotion": "neutral",
            "last_topic": None
        }
    with open(path, "r") as f:
        return json.load(f)


def save_short_term_memory(npc_id: str, data: dict):
    path = os.path.join(MEMORY_DIR, f"{npc_id}_st_mem.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
