from __future__ import annotations

from typing import Callable

from src.core.model import TemplateRecord

Generator = Callable[..., list[TemplateRecord]]


class TemplateRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, Generator] = {}

    def register(self, module_name: str, generator: Generator) -> None:
        self._registry[module_name] = generator

    def modules(self) -> list[str]:
        return sorted(self._registry.keys())

    def list_template_ids(self, module_name: str | None = None) -> list[str]:
        modules = [module_name] if module_name else self.modules()
        template_ids: list[str] = []
        for module in modules:
            generator = self._registry[module]
            template_ids.extend(record.id for record in generator())
        return sorted(template_ids)

    def generate(self, module_name: str, **kwargs: str) -> list[TemplateRecord]:
        if module_name not in self._registry:
            raise ValueError(f"Unknown module: {module_name}")
        return sorted(self._registry[module_name](**kwargs), key=lambda r: r.id)
