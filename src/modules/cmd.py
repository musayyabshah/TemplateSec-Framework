from __future__ import annotations

from src.core.model import TemplateRecord

_ALLOWED_OS = {"linux", "windows", "auto"}


def generate_cmd_templates(os: str = "auto", **_: str) -> list[TemplateRecord]:
    if os not in _ALLOWED_OS:
        raise ValueError(f"Unsupported os selector: {os}")
    selected_os = "linux" if os == "auto" else os

    return [
        TemplateRecord(
            id=f"cmd_separator_{selected_os}",
            module="cmd",
            metadata={"os": selected_os, "pattern_type": "separator-pattern"},
            template=f"{{{{CMD_INJECTION_SEPARATOR_TEMPLATE_{selected_os.upper()}}}}}",
            notes=(
                "Concept-only command separator pattern represented with [[CMD_SEPARATOR]]. Defenders should use direct "
                "API invocation, strict allowlists, and avoid shell interpolation entirely."
            ),
            transforms=["url", "base64", "hex", "whitespace_tokens", "comment_tokens"],
        ),
        TemplateRecord(
            id=f"cmd_chaining_{selected_os}",
            module="cmd",
            metadata={"os": selected_os, "pattern_type": "chaining-pattern"},
            template=f"{{{{CMD_INJECTION_CHAINING_TEMPLATE_{selected_os.upper()}}}}}",
            notes=(
                "Concept-only command chaining study pattern using [[CMD_CHAIN_TOKEN]]. Defenders should tokenize input, "
                "enforce command maps, and sandbox execution contexts where commands are unavoidable."
            ),
            transforms=["url", "base64", "hex", "mixed_encoding"],
        ),
        TemplateRecord(
            id=f"cmd_substitution_{selected_os}",
            module="cmd",
            metadata={"os": selected_os, "pattern_type": "substitution-pattern"},
            template=f"{{{{CMD_INJECTION_SUBSTITUTION_TEMPLATE_{selected_os.upper()}}}}}",
            notes=(
                "Concept-only substitution pattern using [[SUBSTITUTION_TOKEN]]. Defenders should apply strict validation, "
                "disable unsafe interpreters, and isolate privileged operations."
            ),
            transforms=["url", "base64", "hex", "case_variation_description"],
        ),
    ]
