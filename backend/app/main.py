from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.schemas import MessagePayload
from backend.app.intent_router import classify_intent, Intent
from backend.app.router_brain import route_message

from backend.app.timeline.event_bus import event_bus
from backend.app.timeline.integration_npc import register_npc_timeline_reactions
from backend.app.timeline.timeline_engine import timeline_engine
from backend.app.timeline.timeline_runner import timeline_runner
from backend.app.timeline.timeline_loader import load_motown25_timeline

from backend.app.api.timeline_routes import router as timeline_router
from backend.app.api.npc_routes import router as npc_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_npc_timeline_reactions(event_bus)


# --------------------------------
# LIFECYCLE MANAGEMENT (CRITICAL)
# --------------------------------

@app.on_event("startup")
async def startup():
    from backend.app.timeline.timeline_loader import load_motown25_timeline

    timeline_engine.reset()
    timeline_engine.load_events(load_motown25_timeline())

    # 🔑 START AT MICHAEL JACKSON MOMENT
    timeline_engine.start_at(1800)



@app.on_event("shutdown")
async def shutdown():
    # 🧹 Clean shutdown (prevents zombie threads)
    timeline_runner.stop()
    timeline_engine.reset()


# --------------------------------
# API
# --------------------------------

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/route-intent")
async def route_intent(payload: MessagePayload):
    intent = classify_intent(payload.message)
    return {"intent": intent.value}


@app.post("/engine")
async def engine(payload: MessagePayload):
    intent: Intent = classify_intent(payload.message)
    reply = route_message(payload.message, intent)

    return {
        "intent": intent.value,
        "response": reply,
    }


app.include_router(timeline_router)
app.include_router(npc_router)
