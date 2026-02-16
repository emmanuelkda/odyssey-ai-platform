import json
from pathlib import Path
from backend.app.timeline.models import TimelineEvent, EventType

TIMELINE_PATH = Path(__file__).parent / "motown25_timeline.json"


def load_motown25_timeline() -> list[TimelineEvent]:
    with open(TIMELINE_PATH, "r") as f:
        raw_events = json.load(f)

    events = []
    for e in raw_events:
        events.append(
            TimelineEvent(
                id=e["id"],
                t=e["t"],
                type=EventType(e["type"]),
                description=e["description"],
                tags=e.get("tags", []),

                # ✅ SAFE: supports old + new JSON
                npc_reactions=e.get("npc_reactions"),
            )
        )

    return events


def load_events() -> list[TimelineEvent]:
    return load_motown25_timeline()
