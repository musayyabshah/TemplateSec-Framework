from __future__ import annotations

from src.core.model import TemplateRecord

_ALLOWED_DBS = {"mysql", "postgresql", "mssql"}


def generate_sqli_templates(db: str = "mysql", **_: str) -> list[TemplateRecord]:
    if db not in _ALLOWED_DBS:
        raise ValueError(f"Unsupported db selector: {db}")

    return [
        TemplateRecord(
            id=f"sqli_error_{db}",
            module="sqli",
            metadata={"db": db, "type": "error-based"},
            template=f"{{{{SQLI_ERROR_TEMPLATE_{db.upper()}}}}}",
            notes=(
                "Concept-only error-based pattern. Defenders should use parameterized queries, generic error handling, "
                "and strict input validation. Abstract bypass token: [[SQL_COMMENT_TOKEN]]."
            ),
            transforms=["url", "base64", "hex", "keyword_case_variation_description"],
        ),
        TemplateRecord(
            id=f"sqli_union_{db}",
            module="sqli",
            metadata={"db": db, "type": "union-based"},
            template=f"{{{{SQLI_UNION_TEMPLATE_{db.upper()}}}}}",
            notes=(
                "Concept-only union-style structure for defensive study. Defenders should restrict query structure changes, "
                "validate schema-bound inputs, and monitor anomalous query shapes. Abstract token: [[UNION_KEYWORD]]."
            ),
            transforms=["url", "base64", "hex", "comment_token_insertion"],
        ),
        TemplateRecord(
            id=f"sqli_blind_{db}",
            module="sqli",
            metadata={"db": db, "type": "blind"},
            template=f"{{{{SQLI_BLIND_TEMPLATE_{db.upper()}}}}}",
            notes=(
                "Concept-only blind logic description. Defenders should detect timing anomalies, enforce least privilege, "
                "and use prepared statements across all data access paths."
            ),
            transforms=["url", "base64", "hex", "boolean_token_swaps"],
            blind_mode_description=(
                "Educational blind mode concept: compare abstract true/false branches or timing indicators using "
                "[[BOOLEAN_BRANCH_TOKEN]] and [[SLEEP_FUNCTION]]."
            ),
        ),
    ]
