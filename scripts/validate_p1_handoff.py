#!/usr/bin/env python3
"""Validate proposal-only file inventories and legal handoff offline; grant no rights."""

import argparse
import hashlib
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker

from validate_candidates import object_schema, choices
from validate_intake_plan import (DEFAULT_PATH as INTAKE_PATH,
                                  validate as validate_intake)
from validate_p1_readiness import (DEFAULT_PATH as READINESS_PATH, CANDIDATES_PATH,
                                   OWNERS, fingerprint, read_json)
from validate_skills import ROOT, pointer

DEFAULT_PATH = ROOT / "data/reviews/p1-handoff.json"
DECISIONS = ("eligible-for-scope-review", "requires-authorization",
             "exclude-from-hosting", "unverified")
TEXT = {"type": "string", "minLength": 1, "pattern": r"\S"}
SHA = {"type": "string", "pattern": "^[a-f0-9]{40}$"}
DIGEST = {"type": "string", "pattern": "^[a-f0-9]{64}$"}
# Repository-relative, explicit files only. No globs, escapes or external paths.
PATH = {"type": "string", "pattern": r"^(?!/)(?!.*(?:^|/)\.{1,2}(?:/|$))[^\\\x00-\x1f*?\[\]]+$"}


def handoff_schema():
    action = object_schema({"owner": choices(*OWNERS), "action": TEXT})
    return object_schema({
        "format_version": {"type": "integer", "const": 1},
        "task": {"const": "LR-P0-05"},
        "records": {"type": "array", "minItems": 1, "items": object_schema({
            "candidate_id": TEXT, "readiness_snapshot_sha256": DIGEST,
            "intake_snapshot_sha256": DIGEST, "revision": SHA,
            "manifest": PATH, "manifest_sha256": DIGEST,
            "tree_file_count": {"type": "integer", "minimum": 1},
            "tree_sha": SHA,
            "hosting_status": {"const": "not-approved"},
            "professional_status": {"const": "not-performed"},
            "catalog_status": {"const": "not-admitted"},
            "regulatory_currency": object_schema({
                "status": choices("not-checked", "pending-verification"),
                "as_of": {"type": "null"},
            }),
            "unresolved_issues": {"type": "array", "minItems": 1,
                                  "items": object_schema({**action["properties"],
                                      "kind": choices("rights", "dependency", "scope")})},
            "professional_todos": {"type": "array", "minItems": 1,
                                   "items": object_schema({
                                       "owner": {"const": "legal-professional"}, "action": TEXT})},
            "handoff_section": TEXT,
        })},
    })


def manifest_schema():
    return object_schema({
        "format_version": {"type": "integer", "const": 1},
        "candidate_id": TEXT, "revision": SHA, "tree_sha": SHA,
        "files": {"type": "array", "minItems": 1, "items": object_schema({
            "path": PATH, "blob_sha": SHA, "mode": choices("100644", "100755"),
            "file_type": TEXT, "role": TEXT, "purpose": TEXT,
            "content_review": choices("read", "static-scan", "not-read"),
            "decision": choices(*DECISIONS), "basis": TEXT,
        })},
    })


def inventory_tree_sha(files):
    """Rebuild Git's tree hash from path/mode/blob facts, without file contents."""
    tree = {}
    for f in files:
        parts = f["path"].split("/")
        node = tree
        for part in parts[:-1]:
            node = node.setdefault(part, {})
            if not isinstance(node, dict):
                raise ValueError("file/directory path conflict")
        if parts[-1] in node or any(not part for part in parts):
            raise ValueError("duplicate or empty path component")
        node[parts[-1]] = (f["mode"], f["blob_sha"])

    def digest(node):
        entries = []
        for name, value in node.items():
            mode, sha = ("40000", digest(value)) if isinstance(value, dict) else value
            entries.append((name.encode() + (b"/" if mode == "40000" else b""),
                            mode.encode() + b" " + name.encode() + b"\0" + bytes.fromhex(sha)))
        body = b"".join(value for _, value in sorted(entries))
        return hashlib.sha1(b"tree " + str(len(body)).encode() + b"\0" + body).hexdigest()
    return digest(tree)


def load_checked(path, schema):
    try:
        data = read_json(path)
    except (OSError, UnicodeError, ValueError) as exc:
        return None, [f"{path}: /: cannot read UTF-8 JSON: {exc}"]
    errors = [f"{path}: {pointer(e.absolute_path)}: {e.message}" for e in
              Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data)]
    return data, errors


def validate(path=DEFAULT_PATH, candidates_path=CANDIDATES_PATH,
             readiness_path=READINESS_PATH, intake_path=INTAKE_PATH, root=ROOT):
    """Return record count and diagnostics; reuse all original audit/intake gates."""
    path, root = Path(path), Path(root).resolve()
    data, errors = load_checked(path, handoff_schema())
    records = data.get("records", []) if isinstance(data, dict) else []
    count = len(records) if isinstance(records, list) else 0
    _, prior_errors = validate_intake(intake_path, candidates_path, readiness_path)
    if errors or prior_errors:
        return count, errors + prior_errors
    audits = {r["candidate_id"]: r for r in read_json(readiness_path)["records"]}
    proposals = {r["candidate_id"]: r for r in read_json(intake_path)["records"]}
    expected = {cid for cid, p in proposals.items() if p["proposed_track"] == "curated-hosting"}
    seen = set()
    for i, r in enumerate(records):
        def fail(field, message):
            errors.append(f"{path}: /records/{i}/{field}: {message}")
        cid = r["candidate_id"]
        if cid in seen:
            fail("candidate_id", "duplicate candidate ID")
        seen.add(cid)
        if cid not in expected:
            fail("candidate_id", "requires an existing curated-hosting proposal; no blocked upgrades")
            continue
        a, p = audits[cid], proposals[cid]
        for field, value in (("revision", a["revision"]),
                             ("readiness_snapshot_sha256", fingerprint(a)),
                             ("intake_snapshot_sha256", fingerprint(p)),
                             ("regulatory_currency", {k: a["regulatory_currency"][k]
                                                       for k in ("status", "as_of")}),
                             ("handoff_section", cid)):
            if r[field] != value:
                fail(field, "must match fixed audit/proposal; changes require re-review")
        if not {"rights", "dependency"} <= {x["kind"] for x in r["unresolved_issues"]}:
            fail("unresolved_issues", "must retain rights and dependency follow-ups")
        if not {"Human Maintainer", "engineering-maintainer"} <= {x["owner"] for x in r["unresolved_issues"]}:
            fail("unresolved_issues", "must assign maintainer and engineering roles")
        if not set(a["professional_review"]["required_checks"]) <= {x["action"] for x in r["professional_todos"]}:
            fail("professional_todos", "must retain original professional checks")
        mp = (root / r["manifest"]).resolve()
        if (r["manifest"] != f"data/reviews/manifests/{cid}.json"
                or not mp.is_relative_to(root)):
            fail("manifest", "must be the candidate manifest within the repository")
            continue
        m, me = load_checked(mp, manifest_schema())
        errors.extend(me)
        if me:
            continue
        if fingerprint(m) != r["manifest_sha256"]:
            fail("manifest_sha256", "inventory changed; re-review file scope")
        if m["candidate_id"] != cid or m["revision"] != r["revision"]:
            fail("manifest", "inventory must match candidate and original revision")
        files = m["files"]
        try:
            if m["tree_sha"] != r["tree_sha"] or inventory_tree_sha(files) != r["tree_sha"]:
                fail("tree_sha", "path/mode/blob inventory must reconstruct the fixed Git tree")
        except ValueError as exc:
            fail("tree_sha", str(exc))
        if len(files) != r["tree_file_count"]:
            fail("tree_file_count", "inventory count must match recorded fixed tree")
        paths = [f["path"] for f in files]
        if len(set(paths)) != len(paths):
            fail("manifest", "duplicate source path")
        if not {"SKILL.md", "LICENSE", "README.md"} <= set(paths):
            fail("manifest", "must include entry, license and README")
        by_path = {f["path"]: f for f in files}
        prefix = a["source_url"].split("/blob/")[0] + "/blob/" + r["revision"] + "/"
        for evidence in a["audit_evidence"]:
            source_path = evidence["url"].removeprefix(prefix)
            if evidence["blob_sha"] is not None and source_path in by_path:
                if evidence["blob_sha"] != by_path[source_path]["blob_sha"]:
                    fail("manifest", "blob must match existing fixed audit evidence")
        for j, f in enumerate(files):
            if f["decision"] == "eligible-for-scope-review" and f["content_review"] == "not-read":
                errors.append(f"{mp}: /files/{j}/decision: unread content cannot be scope-review eligible")
    if expected != seen:
        errors.append(f"{path}: /records: must cover exactly curated-hosting IDs; missing={sorted(expected-seen)}")
    return count, errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=DEFAULT_PATH)
    parser.add_argument("--candidates", default=CANDIDATES_PATH)
    parser.add_argument("--readiness", default=READINESS_PATH)
    parser.add_argument("--intake", default=INTAKE_PATH)
    parser.add_argument("--root", default=ROOT, help="repository root for inventory paths")
    args = parser.parse_args(argv)
    count, errors = validate(args.path, args.candidates, args.readiness, args.intake, args.root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"FAIL: {len(errors)} error(s) across {count} handoff record(s).", file=sys.stderr)
        return 1
    print(f"PASS: {count} handoff record(s); offline scope/linkage only. "
          "No hosting approval or professional review; regulatory currency remains unverified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
