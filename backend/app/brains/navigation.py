# backend/app/brains/navigation.py

import re
from enum import Enum
from typing import Any, Dict, Optional


class NavAction(str, Enum):
    MOVE_CLOSER = "move_closer"
    MOVE_FARTHER = "move_farther"
    MOVE_TO_ROW = "move_to_row"
    MOVE_TO_SECTION = "move_to_section"
    LOOK_AT_STAGE = "look_at_stage"
    LOOK_LEFT = "look_left"
    LOOK_RIGHT = "look_right"
    UNKNOWN = "unknown_navigation"


def _extract_row(message: str) -> Optional[int]:
    """
    Try to extract a target row from phrases like:
    - 'row 3'
    - 'third row'
    - 'front row'
    - 'back row'
    """
    msg = message.lower()

    # direct numeric: "row 3"
    m = re.search(r"row\s+(\d+)", msg)
    if m:
        try:
            return int(m.group(1))
        except ValueError:
            pass

    # simple words → row numbers (you can tweak this mapping)
    if "front row" in msg or "first row" in msg:
        return 1
    if "second row" in msg:
        return 2
    if "third row" in msg:
        return 3
    if "back row" in msg or "last row" in msg:
        # let the client interpret "back row" however it likes
        return -1  # special marker for "last row"

    return None


def _extract_section(message: str) -> Optional[str]:
    """
    Detect broad sections: left / right / center / middle
    """
    msg = message.lower()

    if "left" in msg:
        return "left"
    if "right" in msg:
        return "right"
    if "center" in msg or "middle" in msg:
        return "center"

    return None


def parse_navigation_command(message: str) -> Dict[str, Any]:
    """
    Turn a natural language message into a structured navigation command.
    """
    msg = message.lower()

    # Look direction / stage focus
    if "look at the stage" in msg or "face the stage" in msg or "look at stage" in msg:
        return {
            "action": NavAction.LOOK_AT_STAGE,
            "target": None,
        }

    if "look left" in msg or "turn left" in msg:
        return {
            "action": NavAction.LOOK_LEFT,
            "target": None,
        }

    if "look right" in msg or "turn right" in msg:
        return {
            "action": NavAction.LOOK_RIGHT,
            "target": None,
        }

    # Move closer / farther
    if "move closer" in msg or "sit closer" in msg or "closer to the stage" in msg:
        return {
            "action": NavAction.MOVE_CLOSER,
            "target": None,
        }

    if "move back" in msg or "farther" in msg or "further back" in msg:
        return {
            "action": NavAction.MOVE_FARTHER,
            "target": None,
        }

    # Move to specific row
    target_row = _extract_row(msg)
    if target_row is not None:
        return {
            "action": NavAction.MOVE_TO_ROW,
            "target": {
                "row": target_row
            },
        }

    # Move to specific section (left/right/center)
    target_section = _extract_section(msg)
    if target_section is not None:
        return {
            "action": NavAction.MOVE_TO_SECTION,
            "target": {
                "section": target_section
            },
        }

    # Default unknown
    return {
        "action": NavAction.UNKNOWN,
        "target": None,
    }


def handle_navigation(message: str) -> Dict[str, Any]:
    """
    High-level handler used by Router Brain.
    Returns a navigation command that the client (Unreal, etc.) can execute.
    """
    cmd = parse_navigation_command(message)

    return {
        "kind": "navigation",
        "action": cmd["action"],
        "target": cmd["target"],
        "raw_message": message,
    }
