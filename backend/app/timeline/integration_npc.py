# backend/app/timeline/integration_npc.py

import threading

from backend.app.timeline.event_bus import OdysseyEventKind, event_bus
from backend.app.timeline.events import TimelineEventPayload
from backend.app.timeline.reaction_store import set_latest_reactions
from backend.app.timeline.context import timeline_context

from backend.app.npc.timeline_reactions import generate_contextual_reaction


# NPCs participating in the timeline
NPC_IDS = [
    "npc_1",
    "npc_2",
    "npc_3",
    "npc_4",
]


def register_npc_timeline_reactions(bus=event_bus):
    """
    Register NPC reaction handler for timeline events.
    """

    def on_timeline_event(payload: TimelineEventPayload):
        """
        Handle a timeline event activation and generate
        context-aware NPC reactions.
        """

        # 🔥 CRITICAL: advance shared timeline context FIRST
        timeline_context.update_for_event(payload.event_id)

        reactions = []

        for npc_id in NPC_IDS:
            text = generate_contextual_reaction(npc_id, payload.event_id)
            if not text:
                continue

            reactions.append(
                {
                    "npc_id": npc_id,
                    "text": text,
                    "event_id": payload.event_id,
                    "t": payload.t,
                }
            )

        # Persist reactions for UI polling
        set_latest_reactions(reactions)

    # Subscribe using the enum (not a string)
    bus.subscribe(
        OdysseyEventKind.TIMELINE_EVENT_ACTIVATED,
        on_timeline_event,
    )
