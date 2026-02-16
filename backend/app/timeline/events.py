from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from backend.app.timeline.models import EventType


class TimelineEventPayload(BaseModel):
    event_id: str
    t: float
    type: EventType
    description: str
    tags: List[str]
    npc_reactions: Optional[List[str]] = None

