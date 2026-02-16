"""
Manual test script for TimelineEngine + TimelineRunner.

Run with:
    python backend/app/timeline/test_timeline_runner.py
"""

import asyncio
from pprint import pprint

from backend.app.timeline.timeline_engine import timeline_engine
from backend.app.timeline.timeline_runner import timeline_runner


async def main():
    print("\n=== ODYSSEY TIMELINE TEST ===\n")

    # Start show + runner
    print("Starting timeline...")
    timeline_engine.start_show()
    timeline_runner.start()

    # Let timeline run for 15 seconds
    for i in range(15):
        await asyncio.sleep(1)

        state = timeline_engine.get_state()
        current_event = timeline_engine.get_current_event()
        next_event = timeline_engine.get_next_event()

        print(f"\n[t={state.show_time:.1f}s]")
        print("Running:", state.is_running)

        if current_event:
            print("Current Event:")
            pprint(current_event.dict())
        else:
            print("Current Event: None")

        if next_event:
            print("Next Event:")
            pprint(next_event.dict())
        else:
            print("Next Event: None")

    # Stop timeline
    print("\nStopping timeline...")
    timeline_runner.stop()
    timeline_engine.pause_show()

    print("\n=== TEST COMPLETE ===\n")


if __name__ == "__main__":
    asyncio.run(main())
