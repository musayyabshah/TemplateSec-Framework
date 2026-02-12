from __future__ import annotations

from src.core.model import TemplateRecord


def generate_xss_templates(**_: str) -> list[TemplateRecord]:
    return [
        TemplateRecord(
            id="xss_reflected_html",
            module="xss",
            metadata={"category": "reflected", "context": "html"},
            template="{{XSS_REFLECTED_HTML_CONTEXT}}",
            notes=(
                "Concept-only reflected input in HTML context. Defenders should apply output encoding, "
                "strict templating, and CSP to reduce unsafe rendering risks."
            ),
            transforms=["url", "base64", "hex", "comment_insertion", "whitespace_tokens", "mixed_encoding"],
        ),
        TemplateRecord(
            id="xss_stored_attribute",
            module="xss",
            metadata={"category": "stored", "context": "attribute"},
            template="{{XSS_STORED_ATTRIBUTE_CONTEXT}}",
            notes=(
                "Concept-only stored input in attribute context. Defenders should validate attributes, enforce allowlists, "
                "and use context-aware encoding."
            ),
            transforms=["url", "base64", "hex", "case_variation_description", "tag_switch_description"],
        ),
        TemplateRecord(
            id="xss_dom_js",
            module="xss",
            metadata={"category": "dom", "context": "js"},
            template="{{XSS_DOM_JS_CONTEXT}}",
            notes=(
                "Concept-only DOM sink flow in script context. Defenders should sanitize DOM writes, avoid unsafe sinks, "
                "and enforce Trusted Types where available."
            ),
            transforms=["url", "base64", "hex", "encoding_layer_description", "context_switch_description"],
        ),
    ]
