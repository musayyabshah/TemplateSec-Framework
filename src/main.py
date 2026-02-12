from __future__ import annotations

import argparse
from pathlib import Path
import sys

from src.core.engine import apply_transform_pipeline
from src.core.registry import TemplateRegistry
from src.exporters.cli import ETHICS_DISCLAIMER, render_cli
from src.exporters.json_exporter import render_json
from src.exporters.txt_exporter import render_txt
from src.modules.cmd import generate_cmd_templates
from src.modules.sqli import generate_sqli_templates
from src.modules.xss import generate_xss_templates
from src.safety.sanitizer import SafetyGateError, validate_safe_content


def build_registry() -> TemplateRegistry:
    registry = TemplateRegistry()
    registry.register("xss", generate_xss_templates)
    registry.register("sqli", generate_sqli_templates)
    registry.register("cmd", generate_cmd_templates)
    return registry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="template-catalog",
        description=(
            "Educational template catalog generator for defensive web security learning. "
            "Outputs placeholders only (non-executable, non-actionable)."
        ),
        epilog=(
            "Examples:\n"
            "  python -m src.main --module xss --format cli --explain\n"
            "  python -m src.main --module sqli --db postgresql --encode base64 --format json --out samples/payloads_sqli.json\n"
            "  python -m src.main --module cmd --os windows --format txt"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--module", choices=["xss", "sqli", "cmd"], default="xss")
    parser.add_argument("--encode", choices=["none", "url", "base64", "hex"], default="none")
    parser.add_argument("--db", choices=["mysql", "postgresql", "mssql"], default="mysql")
    parser.add_argument("--os", choices=["linux", "windows", "auto"], default="auto")
    parser.add_argument("--format", choices=["cli", "json", "txt"], default="cli")
    parser.add_argument("--out", help="Output path; prints to stdout when omitted.")
    parser.add_argument("--list", action="store_true", help="Show available template IDs.")
    parser.add_argument("--explain", action="store_true", help="Include defensive notes and reasoning text.")
    parser.add_argument("--burp-export", help="Optional export-only simulation file path for Burp-style payload list.")
    parser.add_argument("--zap-export", help="Optional export-only simulation file path for OWASP ZAP offline catalog.")
    return parser.parse_args()


def _render_output(fmt: str, records: list, include_explain: bool) -> str:
    if fmt == "cli":
        return render_cli(records, include_explain)
    if fmt == "json":
        return render_json(records, include_explain)
    if fmt == "txt":
        return render_txt(records, include_explain)
    raise ValueError(f"Unsupported format: {fmt}")


def _write_or_print(content: str, out_path: str | None) -> None:
    if out_path:
        path = Path(out_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"Wrote: {path}")
    else:
        print(content, end="")


def _write_simulation_exports(args: argparse.Namespace, records: list) -> None:
    if args.burp_export:
        content = render_txt(records, include_explain=False)
        validate_safe_content(content)
        _write_or_print(content, args.burp_export)
    if args.zap_export:
        metadata = (
            "# OWASP ZAP Offline Catalog\n"
            "mode=offline\n"
            "network_calls=disabled\n"
            f"templates={len(records)}\n"
        )
        content = metadata + render_json(records, include_explain=True)
        validate_safe_content(content)
        _write_or_print(content, args.zap_export)


def main() -> int:
    args = parse_args()
    registry = build_registry()

    if args.list:
        ids = registry.list_template_ids(args.module)
        listing = "\n".join(ids) + "\n"
        validate_safe_content(listing)
        print(ETHICS_DISCLAIMER)
        print(listing, end="")
        return 0

    generator_kwargs: dict[str, str] = {}
    if args.module == "sqli":
        generator_kwargs["db"] = args.db
    if args.module == "cmd":
        generator_kwargs["os"] = args.os

    try:
        records = registry.generate(args.module, **generator_kwargs)
        records = apply_transform_pipeline(records, args.encode)
        output = _render_output(args.format, records, args.explain)
        validate_safe_content(output)
    except (ValueError, SafetyGateError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    _write_or_print(output, args.out)
    _write_simulation_exports(args, records)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
