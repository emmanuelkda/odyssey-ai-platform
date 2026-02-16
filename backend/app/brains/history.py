# backend/app/brains/history.py

from backend.app.truth_engine.retriever import search_facts
from backend.app.timeline.timeline_engine import timeline_engine


class HistoricalQuestionHandler:
    """
    Handles historical fact questions + timeline-aware questions
    for the Odyssey Engine.
    """

    # ---------------------------------------------------------
    # FACT LOOKUP (Truth Engine v1)
    # ---------------------------------------------------------
    def answer_fact_question(self, message: str):
        """
        Takes a raw user message, extracts historical facts,
        and returns a polished narrator-style answer.
        """
        facts = search_facts(message)

        if not facts:
            return "I’m not sure about that detail, but I can look it up in a later version."

        # Auto-format based on fact type
        if "location" in facts:
            return f"Motown 25 took place at the {facts['location']}."

        if "date" in facts:
            return f"Motown 25 was recorded on {facts['date']}."

        if "aired_date" in facts:
            return f"The special aired nationally on {facts['aired_date']}."

        if "song" in facts:
            s = facts["song"]
            return f"'{s['title']}' was performed by {s['performed_by']}."

        if "performer_list" in facts:
            performers = ", ".join(facts["performer_list"])
            return f"Performers included: {performers}."

        if "person" in facts:
            p = facts["person"]
            return f"{p['name']} — {p['bio']}"

        return "I found some information, but I’m not sure how to phrase it yet."

    # ---------------------------------------------------------
    # TIMELINE-AWARE ANSWERS
    # ---------------------------------------------------------
    def answer_now(self):
        """
        Answers: “What’s happening right now?”
        """
        state = timeline_engine.get_state()
        event = timeline_engine.get_current_event()

        if not event:
            return "The show hasn’t started yet."

        t = int(state.show_time)
        return (
            f"Right now we’re {t} seconds into Motown 25. "
            f"{event.description}"
        )

    def answer_next(self):
        """
        Answers: “What comes next?”
        """
        event = timeline_engine.get_next_event()

        if not event:
            return "We’re at the end of the show. Nothing else is scheduled."

        return (
            f"Up next: {event.description} "
            f"(scheduled at t={int(event.t)} seconds)."
        )

    def answer_previous(self):
        """
        Answers: “What just happened?”
        """
        state = timeline_engine.get_state()
        current_t = state.show_time

        prev_event = None
        for e in timeline_engine.events:
            if e.t < current_t:
                prev_event = e
            else:
                break

        if not prev_event:
            return "Nothing has happened yet — the show is just beginning."

        return f"The last thing that happened was: {prev_event.description}"

    def answer_progress(self):
        """
        Answers: “How far into the show are we?”
        """
        state = timeline_engine.get_state()
        minutes = int(state.show_time // 60)
        seconds = int(state.show_time % 60)

        return (
            f"We’re currently {minutes} minutes and {seconds} seconds "
            f"into the Motown 25 special."
        )
