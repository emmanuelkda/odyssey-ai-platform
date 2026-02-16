from backend.app.npc.memory_manager import (
    load_long_term_memory, load_short_term_memory,
    save_long_term_memory, save_short_term_memory
)
from backend.app.npc.response_generator import generate_npc_reply


def handle_npc_interaction(message: str, npc_id: str = "npc_1"):
    # Load memory
    lt_mem = load_long_term_memory(npc_id)
    st_mem = load_short_term_memory(npc_id)

    # Generate reply
    reply_text = generate_npc_reply(message, st_mem, lt_mem)

    # Update ST memory
    st_mem["recent_messages"].append({"user": message, "npc": reply_text})
    st_mem["last_topic"] = message
    st_mem["emotion"] = "engaged"

    save_short_term_memory(npc_id, st_mem)

    return {
        "kind": "npc_speech",
        "speaker": npc_id,
        "text": reply_text,
        "memory": {
            "short_term": st_mem,
            "long_term": lt_mem
        }
    }
