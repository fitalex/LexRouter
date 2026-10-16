#!/usr/bin/env python3
"""Validate one discovery manifest offline; never fetch or execute candidates."""

import argparse
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker

from validate_skills import ROOT, SCHEMA_PATH, pointer


DEFAULT_PATH = ROOT / "data" / "discovery" / "candidates.json"


def object_schema(properties):
    return {"type": "object", "additionalProperties": False,
            "required": list(properties), "properties": properties}


def choices(*values):
    return {"type": "string", "enum": list(values)}


def candidate_schema():
    """Reuse the formal field constraints without relaxing the formal Schema."""
    fields = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))["properties"]
    text = {"type": "string", "minLength": 1, "pattern": r"\S"}
    urls = {"type": "array", "minItems": 1, "uniqueItems": True,
            "items": fields["source_url"]}
    candidate = object_schema({
        "candidate_id": fields["id"],
        "name": fields["name"],
        "description": fields["description"],
        "source_url": fields["source_url"],
        "maintainer": text,
        "business_categories": fields["business_categories"],
        "jurisdiction": object_schema({
            "value": choices("CN-Mainland", "unknown", "other"),
            "status": choices("source-declared", "pending-verification", "verified"),
            "evidence_url": fields["source_url"],
            "notes": text,
        }),
        "runtime": fields["runtime"],
        "runtime_evidence": text,
        "source_verification": object_schema({
            "status": choices("verified-public", "unverified", "unavailable"),
            "checked_at": fields["regulatory_as_of"],
            "revision": text,
            "evidence_urls": urls,
            "notes": text,
        }),
        "authorization": object_schema({
            "status": choices("verified", "pending-verification", "restricted", "not-permitted"),
            "license": text,
            "evidence_urls": urls,
            "notes": text,
        }),
        "regulatory_currency": object_schema({
            "status": choices("not-checked", "pending-verification", "verified"),
            "as_of": {"anyOf": [fields["regulatory_as_of"], {"type": "null"}]},
            "evidence_urls": {"type": "array", "uniqueItems": True,
                              "items": fields["source_url"]},
            "notes": text,
        }),
        "candidate_status": choices("candidate", "needs-evidence", "rejected"),
        "evidence_notes": text,
    })
    candidate["allOf"] = [
        {
            "if": {"properties": {"candidate_status": {"const": "candidate"}}},
            "then": {"properties": {
                "source_verification": {"properties": {"status": {"const": "verified-public"}}},
                "authorization": {"properties": {"status": {"const": "verified"}}},
                "jurisdiction": {"properties": {
                    "value": {"const": "CN-Mainland"},
                    "status": choices("source-declared", "verified"),
                }},
            }},
        },
        {
            "if": {"properties": {"authorization": {
                "properties": {"status": {"const": "not-permitted"}}}}},
            "then": {"properties": {"candidate_status": {"const": "rejected"}}},
        },
    ]
    candidate["properties"]["regulatory_currency"]["allOf"] = [{
        "if": {"properties": {"status": {"const": "verified"}}},
        "then": {"properties": {"as_of": fields["regulatory_as_of"],
                                 "evidence_urls": {"minItems": 1}}},
        "else": {"properties": {"as_of": {"type": "null"}}},
    }]
    return object_schema({
        "format_version": {"type": "integer", "const": 1},
        "candidates": {"type": "array", "items": candidate},
    })


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key {key!r}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"non-JSON constant {value}")


def validate(path):
    """Return (candidate count, diagnostics), preserving file and field positions."""
    path = Path(path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"),
                          object_pairs_hook=unique_object, parse_constant=reject_constant)
    except json.JSONDecodeError as exc:
        return 0, [f"{path}: /: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"]
    except (OSError, UnicodeError, ValueError) as exc:
        return 0, [f"{path}: /: cannot read UTF-8 JSON: {exc}"]

    schema = candidate_schema()
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for error in sorted(validator.iter_errors(data),
                        key=lambda e: (pointer(e.absolute_path), e.message)):
        if error.validator == "required":
            for field in error.validator_value:
                if field not in error.instance:
                    message = f"{path}: {pointer([*error.absolute_path, field])}: required field missing"
                    if message not in errors:
                        errors.append(message)
        else:
            errors.append(f"{path}: {pointer(error.absolute_path)}: {error.message}")

    candidates = data.get("candidates") if isinstance(data, dict) else None
    if not isinstance(candidates, list):
        return 0, errors
    seen = {}
    for index, candidate in enumerate(candidates):
        candidate_id = candidate.get("candidate_id") if isinstance(candidate, dict) else None
        if isinstance(candidate_id, str):
            if candidate_id in seen:
                errors.append(f"{path}: /candidates/{index}/candidate_id: duplicate candidate ID "
                              f"{candidate_id!r}; first seen at /candidates/{seen[candidate_id]}/candidate_id")
            else:
                seen[candidate_id] = index
    return len(candidates), errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=DEFAULT_PATH,
                        help="one UTF-8 candidate manifest (default: data/discovery/candidates.json)")
    args = parser.parse_args(argv)
    try:
        count, errors = validate(args.path)
    except (OSError, UnicodeError, ValueError) as exc:
        count, errors = 0, [f"{SCHEMA_PATH}: /: validation setup error: {exc}"]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"FAIL: {len(errors)} error(s) across {count} candidate record(s).", file=sys.stderr)
        return 1
    print(f"PASS: {count} candidate record(s); structure only "
          "(no network or legal/license verification).")
    if count == 0:
        print("Manifest is empty; this does not demonstrate discovery coverage.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
