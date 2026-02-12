from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class TemplateRecord:
    """A safe, educational template record."""

    id: str
    module: str
    metadata: dict[str, str]
    template: str
    notes: str
    transforms: list[str] = field(default_factory=list)
    blind_mode_description: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        if self.blind_mode_description is None:
            data.pop("blind_mode_description", None)
        return data
