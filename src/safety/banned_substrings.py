from __future__ import annotations

BANNED_SUBSTRINGS: tuple[str, ...] = (
    "<script",
    "javascript:",
    "onerror=",
    "onload=",
    "' or 1=1",
    "\" or 1=1",
    "union select",
    ";",
    "&&",
    "||",
    "|",
    "../",
    "<img",
)
