# TemplateSec Framework (Educational Template Catalog)

## Ethics & Scope Disclaimer

This project is **strictly educational** and intended for **authorized defensive security learning** only.
It follows OWASP-aligned ethical guidance: use only with explicit permission, legal authorization, and defensive intent.
The tool outputs **non-executable placeholders and abstract tokens only**.

## Purpose

TemplateSec Framework is a modular Python CLI that generates a safe catalog of conceptual templates for:

- XSS learning patterns
- SQL injection learning patterns
- Command injection learning patterns

It also includes defensive notes on WAF/filter/validator behavior and modern mitigations.

## Safety Guarantees

- No live requests, scanning, sockets, or API integrations
- No DB drivers or SQL execution
- No command execution paths
- SafetyGate validation blocks banned substrings before export
- Automated tests ensure banned patterns never appear in output

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install pytest
```

## Usage

```bash
python -m src.main --help
python -m src.main --module xss --format cli --explain
python -m src.main --module sqli --db postgresql --encode base64 --format json --out samples/payloads_sqli.json
python -m src.main --module cmd --os windows --format txt --out samples/payloads_cmd.txt
python -m src.main --module xss --list
```

## CLI Flags

- `--module {xss,sqli,cmd}`
- `--encode {none,url,base64,hex}`
- `--db {mysql,postgresql,mssql}` for `sqli`
- `--os {linux,windows,auto}` for `cmd`
- `--format {cli,json,txt}`
- `--out <path>`
- `--list`
- `--explain`
- `--burp-export <path>` export-only simulation list
- `--zap-export <path>` offline catalog simulation (no API calls)

## Architecture

- `src/main.py`: CLI entrypoint
- `src/core/`: model, registry, transform pipeline
- `src/modules/`: xss, sqli, cmd template generators
- `src/transforms/`: encoding and safe obfuscation on placeholder text
- `src/exporters/`: cli/json/txt renderers
- `src/safety/`: banned substrings and SafetyGate validation
- `tests/`: pytest suite for output safety
- `samples/`: generated sample outputs

## Export Instructions

- Standard exports: select `--format` and optional `--out`
- Burp simulation: `--burp-export samples/burp_payload_list.txt`
- OWASP ZAP offline simulation: `--zap-export samples/zap_offline_catalog.txt`

All exports remain placeholder-only and pass SafetyGate checks.
