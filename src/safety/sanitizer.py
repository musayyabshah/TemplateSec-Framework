from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from typing import Any

from src.safety.banned_substrings import BANNED_SUBSTRINGS


class SafetyGateError(ValueError):
    """Raised when potentially unsafe content is detected."""


def _to_text(data: Any) -> str:
    if isinstance(data, str):
        return data
    if is_dataclass(data):
        return json.dumps(asdict(data), sort_keys=True)
    return json.dumps(data, sort_keys=True)


def validate_safe_content(data: Any) -> None:
    text = _to_text(data).lower()
    for banned in BANNED_SUBSTRINGS:
        if banned.lower() in text:
            raise SafetyGateError(
                f"SafetyGate blocked export due to banned substring: {banned}"
            )
