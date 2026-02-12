from __future__ import annotations

from src.core.model import TemplateRecord
from src.transforms.encode import apply_encoding
from src.transforms.obfuscate import apply_safe_obfuscations


def apply_transform_pipeline(
    records: list[TemplateRecord], encode_mode: str
) -> list[TemplateRecord]:
    transformed: list[TemplateRecord] = []
    for record in records:
        encoded_template = apply_encoding(record.template, encode_mode)
        obfuscations = apply_safe_obfuscations(record.template)
        transforms = list(record.transforms)
        if encode_mode != "none":
            transforms = [*transforms, f"encoded:{encode_mode}"]
        transforms = [*transforms, *[f"safe_obfuscation:{k}" for k in sorted(obfuscations.keys())]]
        transformed.append(
            TemplateRecord(
                id=record.id,
                module=record.module,
                metadata=record.metadata,
                template=encoded_template,
                notes=record.notes,
                transforms=transforms,
                blind_mode_description=record.blind_mode_description,
            )
        )
    return transformed
