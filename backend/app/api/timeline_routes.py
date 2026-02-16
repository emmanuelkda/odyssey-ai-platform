# backend/app/api/timeline_routes.py

from fastapi import APIRouter
from backend.app.timeline.timeline_engine import timeline_engine
from backend.app.timeline.reaction_store import get_latest_reactions
from backend.app.timeline.context import timeline_context

router = APIRouter(
    prefix="/timeline",
    tags=["timeline"]
)

@router.get("/state")
def get_timeline_state():
    return {
        "state": {
            "show_time": timeline_engine.show_time,
            "is_running": timeline_engine.next_event is not None,
        },
        "current_event": (
            {
                "id": timeline_engine.current_event.id,
                "description": timeline_engine.current_event.description,
                "tags": timeline_engine.current_event.tags,
            }
            if timeline_engine.current_event
            else None
        ),
        "next_event": (
            {
                "id": timeline_engine.next_event.id,
                "description": timeline_engine.next_event.description,
                "tags": timeline_engine.next_event.tags,
            }
            if timeline_engine.next_event
            else None
        ),
        "crowd_energy": timeline_context.crowd_energy,
        "npc_reactions": get_latest_reactions(),
    }

@router.post("/reset")
def reset_timeline():
    from backend.app.timeline.timeline_runner import timeline_runner
    from backend.app.timeline.timeline_loader import load_motown25_timeline

    timeline_runner.stop()
    timeline_engine.reset()

    events = load_motown25_timeline()
    timeline_engine.load_events(events)
    timeline_engine.start_at(1800)
    timeline_engine.start()
    timeline_runner.start()

    return {"status": "reset"}

@router.get("/state")
def get_timeline_state():
    current_event = timeline_engine.get_current_event()
    next_event = timeline_engine.get_next_event()

    return {
        "show_time": timeline_engine.get_show_time(),
        "current_event": current_event.model_dump() if current_event else None,
        "next_event": next_event.model_dump() if next_event else None,
        "npc_reactions": get_latest_reactions(),
    }

