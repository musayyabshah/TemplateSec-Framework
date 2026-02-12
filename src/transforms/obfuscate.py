from __future__ import annotations


def apply_safe_obfuscations(value: str) -> dict[str, str]:
    return {
        "comment_insertion": value.replace("_", "[[COMMENT]]_"),
        "whitespace_abuse": value.replace("_", "[[WS]]_"),
        "mixed_encoding_note": "Apply URL->Base64 over placeholder text only.",
    }
