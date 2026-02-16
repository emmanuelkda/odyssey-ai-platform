from typing import Any, Dict, Optional

from backend.app.intent_router import Intent, classify_intent

from backend.app.brains.system import handle_system_command
from backend.app.brains.npc import handle_npc
from backend.app.truth_engine.service import answer_question as truth_answer_question

from backend.app.timeline.reaction_store import get_latest_reactions


def route_message(
    user_text: str,
    session_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Flagship-safe router for the public 'odyssey-ai-platform' repo.

    Design goal:
      - Keep the platform narrative tight: routing + truth engine + agent runtime + temporal state
      - Avoid optional 'brains' that create import/packaging dependency whack-a-mole
      - Fail gracefully (product-style) when an unsupported intent is detected
    """
    context = context or {}
    intent: Intent = classify_intent(user_text)

    # Optional: attach the latest timeline reactions if available
    latest_reactions = get_latest_reactions()
    if latest_reactions:
        context["latest_reactions"] = latest_reactions

    if intent == Intent.SYSTEM:
        return handle_system_command(user_text, session_id=session_id, context=context)

    if intent == Intent.HISTORY:
        result = truth_answer_question(user_text)
        if isinstance(result, dict):
            return {"intent": "history", **result}
        return {"intent": "history", "answer": str(result)}

    if intent == Intent.NPC:
        return handle_npc(user_text, session_id=session_id, context=context)

    # Everything else is intentionally not included in the flagship repo
    return {
        "intent": getattr(intent, "value", str(intent)),
        "status": "unsupported_in_flagship_repo",
        "message": (
            "This public flagship repo is intentionally scoped to core platform behaviors "
            "(routing, truth/knowledge, agent runtime, and temporal state). "
            "This request maps to an optional module not included here."
        ),
    }
