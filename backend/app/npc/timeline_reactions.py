# backend/app/npc/timeline_reactions.py

from backend.app.timeline.context import timeline_context

NPC_PERSONALITIES = {
    "npc_1": "superfan",
    "npc_2": "casual",
    "npc_3": "critic",
    "npc_4": "industry",
}

REACTIONS = {
    "show_start": {
        "low": {
            "superfan": "I can feel it building already…",
            "casual": "Looks like things are getting started.",
            "critic": "Let’s see how this opens.",
            "industry": "You can sense anticipation in the room.",
        },
        "medium": {
            "superfan": "This is it. I’ve been waiting for this.",
            "casual": "Okay, now it’s getting interesting.",
            "critic": "Strong opening atmosphere.",
            "industry": "Motown always knew how to warm a crowd.",
        },
    },
    "jackson5_medley": {
        "high": {
            "superfan": "This is unreal. Every song hits.",
            "casual": "Wow—this is way bigger than I expected.",
            "critic": "Tight performance. The crowd’s fully locked in.",
            "industry": "This is the sound that changed pop music.",
        }
    },
}


def generate_contextual_reaction(npc_id: str, event_id: str) -> str | None:
    personality = NPC_PERSONALITIES.get(npc_id)
    if not personality:
        return None

    energy = timeline_context.crowd_energy

    event_reactions = REACTIONS.get(event_id, {})
    energy_reactions = event_reactions.get(energy, {})

    return energy_reactions.get(personality)
