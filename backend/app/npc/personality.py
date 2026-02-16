def apply_personality_traits(text: str, traits: dict) -> str:
    """
    Adjust NPC tone based on personality sliders.
    """
    friendliness = traits.get("friendliness", 0.5)
    excitement = traits.get("excitement", 0.5)
    sarcasm = traits.get("sarcasm", 0.0)
    talk = traits.get("talkativeness", 0.5)

    # Friendly tone
    if friendliness > 0.7:
        text = "Hey! " + text
    elif friendliness < 0.3:
        text = "Look... " + text

    # Excited tone
    if excitement > 0.7:
        text = text + " 🤩"

    # Sarcastic tone
    if sarcasm > 0.6:
        text = text + " (if you even care...)"

    # Talkativeness
    if talk < 0.3:
        text = text.split(".")[0] + "."

    return text
