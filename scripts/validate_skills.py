#!/usr/bin/env python3
"""Validate Skill JSON metadata without downloading or executing Skills."""

import argparse
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "skill.schema.json"


def pointer(parts):
    """Render a JSON Pointer (use / for the document root in diagnostics)."""
    return "/" + "/".join(str(p).replace("~", "~0").replace("/", "~1") for p in parts)


def collect_files(paths):
    files = set()
    errors = []
    for raw in paths:
        path = Path(raw)
        if path.is_file():
            if path.suffix.lower() != ".json":
                errors.append(f"{path}: /: expected a JSON metadata file")
            else:
                files.add(path.resolve())
        elif path.is_dir():
            files.update(p.resolve() for p in path.rglob("*")
                         if p.is_file() and p.suffix.lower() == ".json")
        else:
            errors.append(f"{path}: /: path does not exist or is not a file/directory")
    return sorted(files), errors


def validate(paths):
    """Return (file count, diagnostics); check IDs across the input batch."""
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    files, errors = collect_files(paths)
    seen_ids = {}
    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path}: /: invalid JSON at line {exc.lineno}, "
                          f"column {exc.colno}: {exc.msg}")
            continue
        except (OSError, UnicodeError) as exc:
            errors.append(f"{path}: /: cannot read UTF-8 JSON: {exc}")
            continue

        for error in sorted(validator.iter_errors(data),
                            key=lambda e: (pointer(e.absolute_path), e.message)):
            if error.validator == "required":
                # jsonschema points required errors at the containing object;
                # add each missing field explicitly for actionable diagnostics.
                for field in error.validator_value:
                    if field not in error.instance:
                        message = f"{path}: {pointer([*error.absolute_path, field])}: required field missing"
                        if message not in errors:
                            errors.append(message)
            else:
                errors.append(f"{path}: {pointer(error.absolute_path)}: {error.message}")

        skill_id = data.get("id") if isinstance(data, dict) else None
        if isinstance(skill_id, str):
            if skill_id in seen_ids:
                errors.append(f"{path}: /id: duplicate id {skill_id!r}; "
                              f"first seen in {seen_ids[skill_id]}")
            else:
                seen_ids[skill_id] = path
    return len(files), errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="JSON metadata files or directories (default: skills/)")
    args = parser.parse_args(argv)
    try:
        count, errors = validate(args.paths or [ROOT / "skills"])
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"{SCHEMA_PATH}: /: validation setup/read error: {exc}", file=sys.stderr)
        return 1
    if errors:
        for message in errors:
            print(message, file=sys.stderr)
        print(f"FAIL: {len(errors)} error(s) across {count} metadata file(s).", file=sys.stderr)
        return 1
    if count == 0:
        print("PASS: 0 metadata file(s); directory is empty. Run fixture tests to verify the validator.")
    else:
        print(f"PASS: {count} metadata file(s) validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
