NPC_MEMORY = {
    "npc_1": [],
    "npc_2": []
}

def add_memory(npc_id: str, user_message: str, npc_reply: str):
    # Store last 5 interactions max
    NPC_MEMORY[npc_id].append({"user": user_message, "npc": npc_reply})
    NPC_MEMORY[npc_id] = NPC_MEMORY[npc_id][-5:]  # keep last 5

def get_memory(npc_id: str):
    return NPC_MEMORY.get(npc_id, [])
