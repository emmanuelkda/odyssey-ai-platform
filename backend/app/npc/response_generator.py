from openai import OpenAI
from backend.app.settings import settings
from backend.app.npc.personality import apply_personality_traits

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_npc_reply(message: str, memory: dict, persona: dict):
    """
    Input:
      - message: user input
      - memory: short-term memory
      - persona: long-term memory
    """

    prompt = f"""
You are an NPC inside a VR recreation of Motown 25.

Your personality:
{persona}

Your short-term context:
{memory}

User says: "{message}"

Respond in character as an excited Motown 25 audience member. 
Keep it natural, lively, and immersive.
"""

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
    )

    reply = completion.choices[0].message.content.strip()

    # Apply personality filters (tone, excitement, talkativeness)
    reply = apply_personality_traits(reply, persona["traits"])

    return reply
