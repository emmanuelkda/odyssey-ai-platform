# backend/app/npc/reactions.py

import random
from backend.app.npc.memory_manager import (
    load_long_term_memory,
    load_short_term_memory,
    save_short_term_memory,
)

REACTION_TEMPLATES = {
    "excitement": [
        "Oh wow… {event}!",
        "I can’t believe this is happening — {event}!",
        "This is one of my favorite parts… {event}!",
        "{event}! Incredible!",
    ],
    "surprise": [
        "Wait—did you see that? {event}!",
        "Woah… {event}. I didn't expect that.",
        "{event}? No way!",
    ],
    "calm": [
        "{event}.",
        "{event}… pretty cool.",
        "Hmm… {event}.",
    ],
}


def generate_reaction(npc_id: str, event_name: str):
    """
    Generate an NPC reaction based on personality traits.

    IMPORTANT:
    - This function must NEVER throw.
    - Missing memory files are expected on first run.
    """

    # -------------------------
    # Load long-term memory
    # -------------------------
    try:
        lt = load_long_term_memory(npc_id)
    except FileNotFoundError:
        # Safe default personality
        lt = {
            "traits": {
                "excitement": 0.5,
                "talkativeness": 0.5,
                "sarcasm": 0.0,
            }
        }

    # -------------------------
    # Load short-term memory (FAIL SAFE)
    # -------------------------
    try:
        st = load_short_term_memory(npc_id)
    except FileNotFoundError:
        # Bootstrap short-term memory if missing
        st = {
            "recent_messages": [],
            "emotion": None,
            "last_topic": None,
        }

    traits = lt.get("traits", {})
    excitement = traits.get("excitement", 0.5)
    talkative = traits.get("talkativeness", 0.5)
    sarcasm = traits.get("sarcasm", 0.0)

    # -------------------------
    # 1. Determine if NPC reacts
    # -------------------------
    react_chance = talkative * 0.8 + excitement * 0.4
    if random.random() > react_chance:
        return None  # NPC stays silent

    # -------------------------
    # 2. Choose reaction style
    # -------------------------
    if sarcasm > 0.6:
        template = "{event}. Sure… whatever."
    else:
        if excitement > 0.7:
            style = "excitement"
        elif excitement < 0.3:
            style = "calm"
        else:
            style = random.choice(["excitement", "surprise", "calm"])

        template = random.choice(REACTION_TEMPLATES[style])

    reaction_text = template.format(event=event_name)

    # -------------------------
    # 3. Update short-term memory
    # -------------------------
    st.setdefault("recent_messages", []).append(
        {
            "npc_reaction": reaction_text,
            "event": event_name,
        }
    )
    st["emotion"] = "excited"
    st["last_topic"] = event_name

    # Persist memory safely
    save_short_term_memory(npc_id, st)

    # -------------------------
    # 4. Return reaction payload
    # -------------------------
    return {
        "kind": "npc_reaction",
        "speaker": npc_id,
        "text": reaction_text,
        "event": event_name,
    }
