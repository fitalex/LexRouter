#!/usr/bin/env python3
"""Validate P0-to-P1 audit records offline; never approve legal currency or intake."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker

from validate_candidates import (DEFAULT_PATH as CANDIDATES_PATH, candidate_schema,
                                 choices, object_schema, reject_constant,
                                 unique_object, validate as validate_candidates)
from validate_skills import ROOT, pointer


DEFAULT_PATH = ROOT / "data/discovery/p1-readiness.json"
OWNERS = ("Human Maintainer", "legal-professional", "upstream-rightsholder",
          "engineering-maintainer")


def fingerprint(candidate):
    """Bind the review to every original field, including evidence and statuses."""
    encoded = json.dumps(candidate, sort_keys=True, ensure_ascii=False,
                         separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def readiness_schema():
    fields = candidate_schema()["properties"]["candidates"]["items"]["properties"]
    text = {"type": "string", "minLength": 1, "pattern": r"\S"}
    texts = {"type": "array", "items": text, "uniqueItems": True}
    urls = {"type": "array", "items": fields["source_url"],
            "minItems": 1, "uniqueItems": True}
    sha = {"type": "string", "pattern": "^[0-9a-f]{40}$"}
    issue = object_schema({
        "code": text, "evidence": text, "evidence_urls": urls,
        "impact": text, "next_action": text, "owner": choices(*OWNERS),
    })
    record = object_schema({
        "candidate_id": fields["candidate_id"],
        "candidate_snapshot_sha256": {"type": "string", "pattern": "^[0-9a-f]{64}$"},
        "source_url": fields["source_url"], "revision": sha,
        "business_categories": fields["business_categories"],
        "category_evidence": text,
        "audit_evidence": {"type": "array", "minItems": 1, "items": object_schema({
            "url": fields["source_url"],
            "kind": choices("entry", "documentation", "license", "notice", "tree"),
            "access": choices("read", "not-found"),
            "blob_sha": {"anyOf": [sha, {"type": "null"}]},
            "locator": text, "finding": text,
        })},
        "source_review": object_schema({
            "status": choices("verified-public", "unverified", "unavailable"),
            "entry_exists": {"type": "boolean"},
            "workflow_status": choices("identifiable-workflow", "orchestration-only",
                                       "insufficient-evidence", "out-of-scope"),
            "conclusion": text,
        }),
        "authorization_review": object_schema({
            "status": choices("clear", "missing-license", "conflicting", "restricted",
                              "scope-unclear", "not-permitted"),
            "license": text, "evidence_urls": urls,
            "restrictions": texts, "conclusion": text,
        }),
        "jurisdiction": fields["jurisdiction"],
        "runtime_review": object_schema({
            "value": fields["runtime"],
            "compatibility_status": {"const": "source-declared-unexecuted"},
            "evidence_urls": urls, "conclusion": text,
        }),
        "regulatory_currency": object_schema({
            "status": choices("not-checked", "pending-verification"),
            "as_of": {"type": "null"},
            "evidence_urls": {"type": "array", "uniqueItems": True,
                              "items": fields["source_url"]},
            "notes": text,
        }),
        "professional_review": object_schema({
            "status": {"const": "not-performed"},
            "owner": {"const": "legal-professional"},
            "required_checks": {**texts, "minItems": 1},
        }),
        "blockers": {"type": "array", "items": issue},
        "follow_up": {"type": "array", "minItems": 1, "items": object_schema({
            "owner": choices(*OWNERS), "action": text,
        })},
        "p1_status": choices("ready-for-professional-review", "blocked", "rejected"),
    })
    return object_schema({
        "format_version": {"type": "integer", "const": 1},
        "task": {"const": "LR-P0-03"},
        "audited_at": fields["source_verification"]["properties"]["checked_at"],
        "records": {"type": "array", "minItems": 1, "items": record},
    })


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=unique_object, parse_constant=reject_constant)


def pinned_to(url, source_url, revision):
    """This audit's evidence is limited to the same original GitHub commit."""
    parts = source_url.removeprefix("https://github.com/").split("/")
    if len(parts) < 5 or parts[2] != "blob" or parts[3] != revision:
        return False
    repo = "/".join(parts[:2])
    return (url.startswith(f"https://github.com/{repo}/blob/{revision}/")
            or url == f"https://api.github.com/repos/{repo}/git/trees/{revision}?recursive=1")


def validate(path, candidates_path=CANDIDATES_PATH):
    """Return (record count, file-and-JSON-Pointer diagnostics). No network I/O."""
    path, candidates_path = Path(path), Path(candidates_path)
    try:
        data = read_json(path)
    except json.JSONDecodeError as exc:
        return 0, [f"{path}: /: invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"]
    except (OSError, UnicodeError, ValueError) as exc:
        return 0, [f"{path}: /: cannot read UTF-8 JSON: {exc}"]
    validator = Draft202012Validator(readiness_schema(), format_checker=FormatChecker())
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
    records = data.get("records") if isinstance(data, dict) else None
    count = len(records) if isinstance(records, list) else 0
    # Do not perform relational checks on malformed objects or an invalid source.
    _, candidate_errors = validate_candidates(candidates_path)
    if candidate_errors:
        return count, errors + candidate_errors
    if errors:
        return count, errors
    candidates = {c["candidate_id"]: c for c in read_json(candidates_path)["candidates"]}
    seen = set()

    def fail(index, field, message):
        errors.append(f"{path}: /records/{index}/{field}: {message}")

    for index, record in enumerate(records):
        cid = record["candidate_id"]
        if cid in seen:
            fail(index, "candidate_id", f"duplicate candidate ID {cid!r}")
        seen.add(cid)
        candidate = candidates.get(cid)
        if candidate is None:
            fail(index, "candidate_id", f"unknown candidate ID {cid!r}")
            continue
        if record["candidate_snapshot_sha256"] != fingerprint(candidate):
            fail(index, "candidate_snapshot_sha256", "candidate changed; re-audit all source fields")
        mirrored = {
            "source_url": candidate["source_url"],
            "revision": candidate["source_verification"]["revision"],
            "business_categories": candidate["business_categories"],
            "jurisdiction": candidate["jurisdiction"],
            "regulatory_currency": candidate["regulatory_currency"],
        }
        for field, value in mirrored.items():
            if record[field] != value:
                fail(index, field, "must match original candidate; no silent upgrade or drift")
        if record["runtime_review"]["value"] != candidate["runtime"]:
            fail(index, "runtime_review/value", "must match original candidate runtime")
        auth, source = record["authorization_review"], record["source_review"]
        if auth["license"] != candidate["authorization"]["license"]:
            fail(index, "authorization_review/license", "must preserve original license label")
        if auth["status"] == "clear" and candidate["authorization"]["status"] != "verified":
            fail(index, "authorization_review/status", "unresolved candidate authorization cannot become clear")
        if source["status"] != candidate["source_verification"]["status"]:
            fail(index, "source_review/status", "must match original source verification")
        evidence = record["audit_evidence"]
        observed = {e["url"] for e in evidence}
        if len(observed) != len(evidence):
            fail(index, "audit_evidence", "duplicate evidence URL")
        for j, item in enumerate(evidence):
            if not pinned_to(item["url"], record["source_url"], record["revision"]):
                fail(index, f"audit_evidence/{j}/url", "evidence must pin original repository and revision")
            if item["access"] == "not-found" or item["kind"] == "tree":
                if item["blob_sha"] is not None:
                    fail(index, f"audit_evidence/{j}/blob_sha", "missing paths and trees have no file blob SHA")
            elif item["blob_sha"] is None:
                fail(index, f"audit_evidence/{j}/blob_sha", "read files require a blob SHA")
        entry_found = any(e["kind"] == "entry" and e["access"] == "read"
                          and e["url"] == record["source_url"] for e in evidence)
        if source["entry_exists"] != entry_found:
            fail(index, "source_review/entry_exists", "entry claim must match observed entry evidence")
        for field, links in (("authorization_review/evidence_urls", auth["evidence_urls"]),
                             ("runtime_review/evidence_urls", record["runtime_review"]["evidence_urls"]),
                             ("jurisdiction/evidence_url", [record["jurisdiction"]["evidence_url"]])):
            if any(link not in observed for link in links):
                fail(index, field, "must reference recorded audit evidence")
        for j, blocker in enumerate(record["blockers"]):
            if any(url not in observed for url in blocker["evidence_urls"]):
                fail(index, f"blockers/{j}/evidence_urls", "must reference recorded audit evidence")
        status = record["p1_status"]
        if status in {"blocked", "rejected"} and not record["blockers"]:
            fail(index, "blockers", "blocked/rejected records require evidence, impact, action and owner")
        if status == "ready-for-professional-review":
            if record["blockers"]:
                fail(index, "blockers", "ready records cannot have unresolved blockers")
            if (candidate["candidate_status"] != "candidate"
                    or candidate["authorization"]["status"] != "verified"
                    or auth["status"] != "clear" or source["status"] != "verified-public"
                    or not source["entry_exists"]
                    or source["workflow_status"] != "identifiable-workflow"
                    or record["jurisdiction"]["value"] != "CN-Mainland"):
                fail(index, "p1_status", "ready requires candidate, clear license, entry and independent workflow evidence")
        if (candidate["candidate_status"] == "rejected" or auth["status"] == "not-permitted") and status != "rejected":
            fail(index, "p1_status", "rejected/not-permitted sources must remain rejected")
        owners = {action["owner"] for action in record["follow_up"]}
        if not {"Human Maintainer", "legal-professional"} <= owners:
            fail(index, "follow_up", "must assign maintainer decisions and legal professional review")
    missing = sorted(set(candidates) - seen)
    if missing:
        errors.append(f"{path}: /records: missing candidate IDs: {', '.join(missing)}")
    return count, errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=DEFAULT_PATH)
    parser.add_argument("--candidates", default=CANDIDATES_PATH,
                        help="original candidate manifest (default: data/discovery/candidates.json)")
    args = parser.parse_args(argv)
    try:
        count, errors = validate(args.path, args.candidates)
    except (OSError, UnicodeError, ValueError) as exc:
        count, errors = 0, [f"{args.path}: /: validation setup error: {exc}"]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"FAIL: {len(errors)} error(s) across {count} readiness record(s).", file=sys.stderr)
        return 1
    print(f"PASS: {count} readiness record(s); offline structure and candidate linkage only. "
          "No legal/license verification or intake approval; professional review remains required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
