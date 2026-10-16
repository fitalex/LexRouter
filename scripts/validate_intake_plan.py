#!/usr/bin/env python3
"""Check P0 intake proposals offline; this contract cannot grant approvals."""

import argparse
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker

from validate_candidates import choices, object_schema
from validate_p1_readiness import (CANDIDATES_PATH, DEFAULT_PATH as READINESS_PATH,
                                   OWNERS, fingerprint, read_json,
                                   validate as validate_readiness)
from validate_skills import ROOT, SCHEMA_PATH, pointer


DEFAULT_PATH = ROOT / "data/intake/p1-proposals.json"
GATES = ("mode-scope-decision", "rights-or-originality-review",
         "professional-jurisdiction-currency-review", "deduplication-and-schema",
         "maintainer-catalog-pr")


def intake_schema():
    fields = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))["properties"]
    text = {"type": "string", "minLength": 1, "pattern": r"\S"}
    texts = {"type": "array", "minItems": 1, "uniqueItems": True, "items": text}
    # Explicitly proposal-only. Future approvals require a separately reviewed,
    # evidence-bearing contract, not loosening a status in this P0 snapshot.
    approvals = object_schema({
        "proposal": {"const": "proposed"},
        "authorization": choices("pending", "blocked"),
        "legal_professional": {"const": "not-performed"},
        "hosting": {"const": "not-approved"},
        "catalog": {"const": "not-admitted"},
        "evaluation": {"const": "not-performed"},
        "routing": {"const": "not-assessed"},
    })
    rights = object_schema({
        "copy": {"type": "boolean", "const": False},
        "redistribute": {"type": "boolean", "const": False},
    })
    actions = {"type": "array", "minItems": 1, "items": object_schema({
        "owner": choices(*OWNERS), "action": text,
    })}
    gates = {"type": "array", "minItems": 1, "uniqueItems": True,
             "items": choices(*GATES, "full-hosting-scope-approval",
                              "independent-requirements-design-tests")}
    record = object_schema({
        "candidate_id": fields["id"],
        "readiness_snapshot_sha256": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
        "proposed_track": choices("curated-hosting", "external-reference"),
        "business_value_and_rationale": text,
        "authorization_basis": object_schema({
            "reference": {"const": "p1-readiness.authorization_review"},
            "proposed_use_review": {"const": "not-performed"},
        }),
        "approvals": approvals, "permissions": rights,
        "required_gates": gates, "next_actions": actions,
    })
    opportunity = object_schema({
        "opportunity_id": {**fields["id"], "pattern": "^original-[a-z0-9]+(?:-[a-z0-9]+)*$"},
        "proposed_track": {"const": "original-development"},
        "related_candidate_ids": {"type": "array", "minItems": 1, "uniqueItems": True,
                                  "items": fields["id"]},
        "business_problem": text, "expected_deliverables": texts,
        "independent_design_sources": texts,
        "independence_boundary": text,
        "authorization_basis": {"const": "not-inherited"},
        "development_status": {"const": "not-started"},
        "approvals": approvals, "permissions": rights,
        "required_gates": gates, "next_actions": actions,
    })
    return object_schema({
        "format_version": {"type": "integer", "const": 1},
        "task": {"const": "LR-P0-04"},
        "records": {"type": "array", "minItems": 1, "items": record},
        "original_opportunities": {"type": "array", "items": opportunity},
    })


def validate(path, candidates_path=CANDIDATES_PATH, readiness_path=READINESS_PATH):
    """Return (proposal count, diagnostics), delegating the existing audit checks."""
    path = Path(path)
    try:
        data = read_json(path)
    except json.JSONDecodeError as exc:
        return 0, [f"{path}: /: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"]
    except (OSError, UnicodeError, ValueError) as exc:
        return 0, [f"{path}: /: cannot read UTF-8 JSON: {exc}"]

    errors = [f"{path}: {pointer(e.absolute_path)}: {e.message}" for e in
              Draft202012Validator(intake_schema(), format_checker=FormatChecker()).iter_errors(data)]
    records = data.get("records") if isinstance(data, dict) else None
    count = len(records) if isinstance(records, list) else 0
    # LR-P0-03 already validates candidate evidence, snapshots and readiness.
    _, audit_errors = validate_readiness(readiness_path, candidates_path)
    if errors or audit_errors:
        return count, errors + audit_errors
    audits = {r["candidate_id"]: r for r in read_json(readiness_path)["records"]}
    seen = set()

    def fail(section, index, field, message):
        errors.append(f"{path}: /{section}/{index}/{field}: {message}")

    for index, record in enumerate(records):
        cid = record["candidate_id"]
        if cid in seen:
            fail("records", index, "candidate_id", f"duplicate candidate ID {cid!r}")
        seen.add(cid)
        audit = audits.get(cid)
        if audit is None:
            fail("records", index, "candidate_id", f"unknown candidate ID {cid!r}")
            continue
        if record["readiness_snapshot_sha256"] != fingerprint(audit):
            fail("records", index, "readiness_snapshot_sha256", "audit changed; re-review proposal")
        blocked = audit["p1_status"] != "ready-for-professional-review"
        expected = "blocked" if blocked else "pending"
        if record["approvals"]["authorization"] != expected:
            fail("records", index, "approvals/authorization", "must preserve audit blocking status")
        if record["proposed_track"] == "curated-hosting" and blocked:
            fail("records", index, "proposed_track", "blocked/rejected candidate must remain external-reference in P0")
    missing = sorted(set(audits) - seen)
    if missing:
        errors.append(f"{path}: /records: missing candidate IDs: {', '.join(missing)}")

    opportunity_ids = set()
    for index, opportunity in enumerate(data["original_opportunities"]):
        oid = opportunity["opportunity_id"]
        if oid in opportunity_ids or oid in audits:
            fail("original_opportunities", index, "opportunity_id", "duplicate or third-party ID")
        opportunity_ids.add(oid)
        for cid in opportunity["related_candidate_ids"]:
            if cid not in audits:
                fail("original_opportunities", index, "related_candidate_ids", f"unknown candidate ID {cid!r}")
        if opportunity["approvals"]["authorization"] != "pending":
            fail("original_opportunities", index, "approvals/authorization", "original opportunity cannot inherit third-party authorization")

    for section in ("records", "original_opportunities"):
        for index, record in enumerate(data[section]):
            required = set(GATES)
            if record["proposed_track"] == "curated-hosting":
                required.add("full-hosting-scope-approval")
            if section == "original_opportunities":
                required.add("independent-requirements-design-tests")
            if not required <= set(record["required_gates"]):
                fail(section, index, "required_gates", "missing required approval gates")
            owners = {a["owner"] for a in record["next_actions"]}
            if not {"Human Maintainer", "legal-professional", "engineering-maintainer"} <= owners:
                fail(section, index, "next_actions", "must assign maintainer, legal and engineering responsibilities")
    return count, errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=DEFAULT_PATH)
    parser.add_argument("--candidates", default=CANDIDATES_PATH)
    parser.add_argument("--readiness", default=READINESS_PATH)
    args = parser.parse_args(argv)
    try:
        count, errors = validate(args.path, args.candidates, args.readiness)
    except (OSError, UnicodeError, ValueError) as exc:
        count, errors = 0, [f"{args.path}: /: validation setup error: {exc}"]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"FAIL: {len(errors)} error(s) across {count} intake proposal(s).", file=sys.stderr)
        return 1
    print(f"PASS: {count} candidate proposal(s); offline structure/linkage only. "
          "No hosting, legal, catalog, execution or redistribution approval.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
