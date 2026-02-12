from __future__ import annotations

from src.core.model import TemplateRecord


ETHICS_DISCLAIMER = (
    "[ETHICS] Authorized educational and defensive use only. "
    "Follow OWASP-aligned legal and ethical testing practices."
)


def render_cli(records: list[TemplateRecord], include_explain: bool) -> str:
    lines = [ETHICS_DISCLAIMER, ""]
    for record in records:
        lines.append(f"- id: {record.id}")
        lines.append(f"  module: {record.module}")
        for key, value in sorted(record.metadata.items()):
            lines.append(f"  {key}: {value}")
        lines.append(f"  template: {record.template}")
        lines.append(f"  transforms: {', '.join(record.transforms)}")
        if include_explain:
            lines.append(f"  notes: {record.notes}")
            if record.blind_mode_description:
                lines.append(
                    f"  blind_mode_description: {record.blind_mode_description}"
                )
        lines.append("")
    return "\n".join(lines).strip() + "\n"
