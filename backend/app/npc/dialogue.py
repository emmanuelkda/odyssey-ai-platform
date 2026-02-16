from openai import OpenAI
from backend.app.settings import settings
from backend.app.npc.personas import NPC_PERSONAS
from backend.app.npc.memory import get_memory, add_memory
from backend.app.truth_engine.retriever import search_facts

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_npc_reply(npc_id: str, message: str) -> str:
    persona = NPC_PERSONAS[npc_id]
    memory = get_memory(npc_id)

    # 1. Try Truth Engine first if question is factual
    facts = search_facts(message)
    factual_context = ""

    if facts:
        factual_context = format_facts(facts)

    # 2. Build prompt for LLM
    memory_text = "\n".join(
        [f"User: {m['user']}\nYou ({persona['name']}): {m['npc']}" for m in memory]
    )

    prompt = f"""
You are {persona['name']}, age {persona['age']}, sitting at {persona['seat']}.

Personality: {persona['personality']}.
Tone: {persona['tone']}.
Backstory: {persona['backstory']}.
Knowledge limits: {persona['knowledge_limits']}.

You are an audience member at Motown 25, on March 25, 1983.
You do NOT know anything after 1983.

Conversation memory:
{memory_text}

If the user asks anything factual about Motown, use these facts:
{factual_context}

User says: "{message}"

Respond as {persona['name']} would, in 1–3 short sentences.
Keep it natural, conversational, and true to 1983.
    """

    reply = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
    ).choices[0].message.content.strip()

    # Save memory
    add_memory(npc_id, message, reply)

    return reply


def format_facts(facts):
    lines = []
    for f in facts:
        if "title" in f:
            lines.append(f"Song: {f['title']} performed by {f['performed_by']}.")

        if "location" in f:
            lines.append(f"Event location: {f['location']}.")

        if "event_date" in f:
            lines.append(f"Event date: {f['event_date']}.")

    return "\n".join(lines)
