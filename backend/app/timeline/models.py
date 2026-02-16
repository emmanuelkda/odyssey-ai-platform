# backend/app/timeline/models.py

from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class EventType(str, Enum):
    SHOW_EVENT = "SHOW_EVENT"
    PERFORMANCE_EVENT = "PERFORMANCE_EVENT"
    TRANSITION_EVENT = "TRANSITION_EVENT"


class TimelineEvent(BaseModel):
    id: str
    t: float
    type: EventType
    description: str
    tags: List[str] = []

    # ✅ ADD THIS (this is the missing piece)
    npc_reactions: Optional[List[str]] = None

