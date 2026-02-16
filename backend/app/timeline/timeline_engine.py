from __future__ import annotations
from typing import List, Optional
import time

from backend.app.timeline.models import TimelineEvent
from backend.app.timeline.events import TimelineEventPayload
from backend.app.timeline.event_bus import event_bus, OdysseyEventKind


class TimelineEngine:
    def __init__(self):
        self.events: List[TimelineEvent] = []
        self.start_epoch: float | None = None
        self.start_offset: float = 0.0

    # ------------------------
    # Lifecycle
    # ------------------------

    def load_events(self, events: List[TimelineEvent]):
        self.events = sorted(events, key=lambda e: e.t)

    def start_at(self, t: float):
        """
        Start the timeline as if show time == t
        """
        self.start_offset = t
        self.start_epoch = time.time()

    def reset(self):
        self.start_epoch = None
        self.start_offset = 0.0

    # ------------------------
    # Time
    # ------------------------

    def get_show_time(self) -> float:
        if self.start_epoch is None:
            return 0.0
        return (time.time() - self.start_epoch) + self.start_offset

    # ------------------------
    # Events
    # ------------------------

    def get_current_event(self) -> Optional[TimelineEvent]:
        now = self.get_show_time()
        current = None

        for e in self.events:
            if e.t <= now:
                current = e
            else:
                break

        return current

    def get_next_event(self) -> Optional[TimelineEvent]:
        now = self.get_show_time()
        for e in self.events:
            if e.t > now:
                return e
        return None

    def emit_if_changed(self, last_event_id: Optional[str]) -> Optional[str]:
        """
        Emits event only when it changes (for NPC reactions)
        """
        current = self.get_current_event()
        if not current:
            return last_event_id

        if current.id != last_event_id:
            payload = TimelineEventPayload(
                event_id=current.id,
                t=current.t,
                type=current.type,
                description=current.description,
                tags=current.tags,
                npc_reactions=current.npc_reactions or [],
            )

            event_bus.emit(
                OdysseyEventKind.TIMELINE_EVENT_ACTIVATED,
                payload,
            )
            return current.id

        return last_event_id


# SINGLE authoritative instance
timeline_engine = TimelineEngine()
