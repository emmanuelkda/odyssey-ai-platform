# backend/app/timeline/context.py

import time


class TimelineContext:
    """
    Shared, evolving context for the show.
    """

    def __init__(self):
        self.last_event_id: str | None = None
        self.energy: float = 0.2  # start calm
        self.last_updated: float = time.time()

    def update_for_event(self, event_id: str):
        """
        Event-based energy nudges.
        """
        self.last_event_id = event_id

        if event_id == "show_start":
            self.energy = min(1.0, self.energy + 0.25)
        elif event_id == "jackson5_medley":
            self.energy = min(1.0, self.energy + 0.45)

        self.last_updated = time.time()

    def decay(self):
        """
        Gradual energy decay over time.
        """
        now = time.time()
        delta = now - self.last_updated

        # decay rate tuned for realism
        self.energy = max(0.0, self.energy - (delta * 0.02))
        self.last_updated = now

    @property
    def crowd_energy(self) -> str:
        if self.energy < 0.34:
            return "low"
        elif self.energy < 0.67:
            return "medium"
        return "high"


timeline_context = TimelineContext()
