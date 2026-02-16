# backend/app/timeline/event_bus.py

from enum import Enum
from typing import Any, Callable, Dict, List


class OdysseyEventKind(str, Enum):
    TIMELINE_EVENT_ACTIVATED = "TIMELINE_EVENT_ACTIVATED"


class EventBus:
    def __init__(self) -> None:
        self._subscribers: Dict[OdysseyEventKind, List[Callable[[Any], Any]]] = {}

    def subscribe(self, kind: OdysseyEventKind, handler: Callable[[Any], Any]) -> None:
        self._subscribers.setdefault(kind, []).append(handler)

    def emit(self, kind: OdysseyEventKind, payload: Any) -> List[Any]:
        """Emit an event and collect handler results."""
        results: List[Any] = []

        for handler in self._subscribers.get(kind, []):
            try:
                result = handler(payload)
                if result:
                    results.extend(result)
            except Exception as exc:
                print(f"[EventBus] Error in handler for {kind}: {exc}")

        return results


event_bus = EventBus()
