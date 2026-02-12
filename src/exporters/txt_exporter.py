from __future__ import annotations

from src.core.model import TemplateRecord


def render_txt(records: list[TemplateRecord], include_explain: bool) -> str:
    lines: list[str] = []
    for record in records:
        base = f"{record.id} :: {record.template} :: {record.module}"
        if include_explain:
            base += f" :: {record.notes}"
        lines.append(base)
    return "\n".join(lines) + "\n"
