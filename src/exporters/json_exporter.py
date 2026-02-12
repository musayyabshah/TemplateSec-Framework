from __future__ import annotations

import json

from src.core.model import TemplateRecord


def render_json(records: list[TemplateRecord], include_explain: bool) -> str:
    payload = []
    for record in records:
        entry = record.to_dict()
        if not include_explain:
            entry.pop("notes", None)
            entry.pop("blind_mode_description", None)
        payload.append(entry)
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"
