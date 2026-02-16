from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class MessagePayload(BaseModel):
    message: str


class EngineResponse(BaseModel):
    text: str
    npc_reactions: Optional[List[Any]] = None
    metadata: Optional[Dict[str, Any]] = None
