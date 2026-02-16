# backend/app/timeline/reaction_store.py

from typing import Any, Dict, List, Optional
from threading import Lock
import time

_lock = Lock()

# How long a reaction stays visible (seconds)
REACTION_TTL = 6.0

# Max reactions visible at once
MAX_VISIBLE_REACTIONS = 4

# Internal store
_latest_reactions: List[Dict[str, Any]] = []


def set_latest_reactions(reactions: Optional[List[Dict[str, Any]]]) -> None:
    """
    Store NPC reactions with TTL + density control.
    """
    global _latest_reactions

    now = time.time()

    with _lock:
        # 1. Prune expired reactions
        _latest_reactions[:] = [
            r for r in _latest_reactions
            if r.get("_expires_at", 0) > now
        ]

        if not reactions:
            return

        # 2. Add new reactions with expiry
        for r in reactions:
            if not isinstance(r, dict):
                continue
            if "npc_id" not in r or "text" not in r:
                continue

            r["_expires_at"] = now + REACTION_TTL
            _latest_reactions.append(r)

        # 3. Enforce max visible reactions
        _latest_reactions[:] = _latest_reactions[-MAX_VISIBLE_REACTIONS:]


def get_latest_reactions() -> List[Dict[str, Any]]:
    """
    Return active (non-expired) reactions for UI.
    """
    now = time.time()

    with _lock:
        _latest_reactions[:] = [
            r for r in _latest_reactions
            if r.get("_expires_at", 0) > now
        ]

        # Remove internal fields before returning
        return [
            {k: v for k, v in r.items() if not k.startswith("_")}
            for r in _latest_reactions
        ]
