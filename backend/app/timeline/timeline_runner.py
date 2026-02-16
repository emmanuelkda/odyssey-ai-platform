import threading
import time

from backend.app.timeline.timeline_engine import timeline_engine


class TimelineRunner:
    def __init__(self, tick_interval: float = 1.0):
        self.tick_interval = tick_interval
        self._thread: threading.Thread | None = None
        self._running = False

    def start(self):
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False

    def _loop(self):
        while self._running:
            timeline_engine.tick(self.tick_interval)
            time.sleep(self.tick_interval)
            
            


timeline_runner = TimelineRunner()
