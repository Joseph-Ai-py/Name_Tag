"""JSON parsing utilities."""
import json
import re
from typing import Any


def extract_json(text: str) -> dict[str, Any] | None:
    """
    Parse JSON from fenced blocks, inline body, or raw text.

    Attempts three strategies:
    1. Extract JSON from markdown code blocks (```json ... ```)
    2. Extract JSON from text between first { and last }
    3. Parse entire text as JSON

    Args:
        text: Text containing JSON

    Returns:
        Parsed JSON dictionary or None if parsing fails
    """
    # Strategy 1: Code block with json marker
    match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Strategy 2: Extract JSON between first { and last }
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            pass

    # Strategy 3: Parse entire text as JSON
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        return None
