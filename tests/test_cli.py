from __future__ import annotations

import json
import subprocess
import sys

from src.safety.banned_substrings import BANNED_SUBSTRINGS


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "src.main", *args],
        check=False,
        capture_output=True,
        text=True,
    )


def test_help_contains_examples() -> None:
    result = run_cli("--help")
    assert result.returncode == 0
    assert "Examples:" in result.stdout


def test_list_mode_outputs_ids() -> None:
    result = run_cli("--module", "xss", "--list")
    assert result.returncode == 0
    assert "xss_reflected_html" in result.stdout


def test_json_output_is_structured_and_safe() -> None:
    result = run_cli("--module", "sqli", "--db", "mysql", "--format", "json", "--explain")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert all(item["template"].startswith("{{") for item in payload)

    lowered = result.stdout.lower()
    for banned in BANNED_SUBSTRINGS:
        assert banned.lower() not in lowered


def test_cmd_default_os_auto_uses_linux_selector() -> None:
    result = run_cli("--module", "cmd", "--format", "json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert all(item["metadata"]["os"] == "linux" for item in payload)


def test_encode_hex_applies_to_placeholder_only() -> None:
    result = run_cli("--module", "xss", "--encode", "hex", "--format", "json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    first_template = payload[0]["template"]
    assert first_template.startswith("7b7b")
